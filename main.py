from flask import Flask, render_template, url_for, redirect, flash, session, g, abort
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm, AdminForm

DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = 'gartic'
MAX_CONTENT_LENGTH = 1024*1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route('/')
@app.route('/index') 
def index():
    return render_template(
        'index.html', title='Reaction app', content='circles screen', menu=dbase.get_menu(), session=session
    )


@app.route('/leaders')
def leaderboard():
    return render_template(
        'leaderboard.html', title='Leaderboard', scoring='0',
        menu=dbase.get_menu(), session=session, leaders=dbase.get_leaders()
    )


@app.route('/profile')
def selfprofile():
    username = current_user.username()
    return render_template(
        'profile.html', username=username, stats=dbase.get_stats(username), menu=dbase.get_menu(), session=session
    )


@app.route('/profile/<username>')
def profile(username):
    return render_template(
        'profile.html', username=username, current_user=current_user,
        stats=dbase.get_stats(username), menu=dbase.get_menu(), session=session
    )


@login_required
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    form = AdminForm()

    if dbase.get_user(current_user.get_id())['admin'] == 1:

        if form.validate_on_submit():
            if form.add.data:
                if form.newusername.data and form.newpassword.data:
                    dbase.add_new(form.newusername.data, generate_password_hash(form.newpassword.data))
            if form.remove.data:
                if form.username.data:
                    dbase.remove(username=form.username.data)
                if form.id.data:
                    dbase.remove(user_id=form.id.data)
            if form.changename.data:
                if form.newusername.data and form.username.data:
                    dbase.change_name(username=form.username.data, new=form.newusername.data)
                if form.newusername.data and form.id.data:
                    dbase.change_name(user_id=form.id.data, new=form.newusername.data)
            if form.changepass.data:
                if form.newpassword.data and form.username.data:
                    dbase.change_password(username=form.username.data, new=generate_password_hash(form.newpassword.data))
                if form.newpassword.data and form.id.data:
                    dbase.change_password(user_id=form.id.data, new=generate_password_hash(form.newpassword.data))
            if form.changeresult.data:
                if form.newresult.data and form.username.data:
                    dbase.change_result(username=form.username.data, new=form.newresult.data)
                if form.newresult.data and form.id.data:
                    dbase.change_result(user_id=form.id.data, new=form.newresult.data)
            if form.setadmin.data:
                if form.username.data:
                    dbase.op(username=form.username.data)
                if form.id.data:
                    dbase.op(user_id=form.id.data)
            if form.removeadmin.data:
                if form.username.data:
                    dbase.op(username=form.username.data, admin=0)
                if form.id.data:
                    dbase.op(user_id=form.id.data, admin=0)

        return render_template('admin.html', title='admin panel', base=dbase.get_all_users(), form=form)
    else:
        abort(403)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username()))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_name(form.username.data)
        if user and check_password_hash(user['password'], form.password.data):
            userlogin = UserLogin().create(user)
            rem = form.remember.data
            login_user(userlogin, remember=rem)
            return redirect(url_for('profile', username=current_user.username()))
        else:
            flash('Incorrect input')
    return render_template('login.html', menu=dbase.get_menu(), form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username()))

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            hash = generate_password_hash(form.password.data)
            res = dbase.add_new(form.username.data, hash)
            if res: 
                flash('Success')
                return redirect(url_for('login'))
        flash('Incorrect input')
    return render_template('signup.html', menu=dbase.get_menu(), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
