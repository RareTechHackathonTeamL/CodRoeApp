from flask import Flask, render_template, redirect, request, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import os
import pymysql
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

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
    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')
    # Userテーブルからemailに一致するユーザを取得
    user = User.query.filter_by(email=email).first()
    if user == None:
        flash('Eメールアドレスまたはパスワードが間違っています。')
        return render_template('login.html')
    else:
        if check_password_hash(user.password, password):
            login_user(user)
            user_name = user.user_name
            flash( user_name + 'さん！おかえりなさい！')
            return render_template('home.html')
        else:
            flash('Eメールアドレスまたはパスワードが間違っています。')
            return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('login_view'))

@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_process():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation') 
    registered_user = User.query.filter_by(email=email).first()
    registered_name = User.query.filter_by(user_name=user_name).first()

    if registered_user != None:
        flash('既にユーザ登録されているようです。')
    elif registered_name != None:
        flash('同じユーザ名のユーザが存在します。別の名前で登録してください。')
    elif user_name == '' or email =='' or password == '' or passwordConfirmation == '':
            flash('空のフォームがあるようです。')
    elif password != passwordConfirmation:
        flash('入力された2つのパスワードが一致しません。')
    else:
        user = User(
            user_id = uuid.uuid4(),
            user_name = request.form.get('user_name'),
            email = request.form.get('email'),
            password = generate_password_hash(password),
            created_at = '2025-07-24'
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        db.session.close()
        flash( 'ようこそ！' + user_name + 'さん！ユーザを登録しました。')
        return render_template('home.html')
    return render_template('register.html')

@app.route('/chat', methods=['GET'])
def chat_view():
    return render_template('home.html')
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)