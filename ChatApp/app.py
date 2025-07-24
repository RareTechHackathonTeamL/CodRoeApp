from flask import Flask, render_template, redirect, request, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import os
import pymysql
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testuser:testuser@MySQL/chatapp'
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods=['GET'])
def top():
    return render_template('register.html')

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
        return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return render_template('new.html')

@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    #if request.method == 'POST':
        # password = request.form.get('password')
        user = User(
            user_id = uuid.uuid4(),
            user_name = request.form.get('user_name'),
            email = request.form.get('email'),
            password = request.form.get('password'),
            created_at = '2025-07-24'
            # passwordConfirmation = request.form.get('password-confirmation'),
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        db.session.close()
        flash('ユーザを登録しました。')
        return render_template('home.html')
    #else:
    #    return render_template('register.html')
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)