from flask import *
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from adapters import *
from adapters.repo import *
from adapters import repo
import sys

sys.path.append('../')
from app import *

user_bp = Blueprint(
    'user_bp', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html',user=None)
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        check_user = repo.repo_instance.get_user(username)
        if check_user == None:
            flash("The user does not exist!")
            return redirect(url_for('user_bp.login'))
        auth = check_password_hash(check_user.password, password)
        if auth == False:
            flash("Incorrect Password!")
            return redirect(url_for('user_bp.login'))
        session['username'] = username

        return redirect(url_for('index'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html', user=session.get('user'))
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        check_user = repo.repo_instance.get_user(username)

        if check_user != None:
            flash("The username has been registered")
            return redirect(url_for('user_bp.register'))
        password_hash = generate_password_hash(password)
        newuser = User(username, password_hash, email)
        repo.repo_instance.add_user(newuser)
        return redirect(url_for('user_bp.login'))


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@user_bp.route('/username%<username>', methods=['GET', 'POST'])
def profile(username):
    user = None
    for u in repo.repo_instance._users:
        if u.username == username:
            user = u
    return render_template("user.html", user=user)


@user_bp.route('/changeprofilepic%<username>', methods=['GET', 'POST'])
def change_pic(username, img=None):
    user = None
    img = img
    for u in repo.repo_instance._users:
        if u.username == username:
            user = u
    if img == None:
        img = user.profile_pic

    if request.method == 'GET':
        return render_template('userpic.html', user=user, img=img)
    elif request.method == 'POST':
        f = request.files.get('pic')
        basepath = os.path.dirname(__file__)[:-5]  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/img/profile_pic',
                                   secure_filename(f.filename))
        f.save(upload_path)
        path = '/static/img/profile_pic/' + secure_filename(f.filename)
        print(path)
        repo.repo_instance.reset_profile(username,path)

        return redirect(url_for("user_bp.change_pic", username=username))


