from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///chatapp.db'
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # Userテーブルからemailに一致するユーザを取得
        user = User.query.filter_by(email = email).first()
        if db.check_password_hash(user.password, password):
            login_user(user)
            flash('ログインに成功しました。')
            return redirect('/chat')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            user_name = request.form.get('user_name'),
            email = request.form.get('email'),
            password = request.form.get('password'),
            passwordConfirmation = request.form.get('password-confirmation'),
        )
        db.session.add(user)
        db.session.commit()
        flash('ユーザを登録しました。')
        return render_template('/login.html')
    else:
            return render_template('/register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)