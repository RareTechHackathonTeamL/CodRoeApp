from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Chat, Message
import pymysql
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from __init__ import create_app, login_manager, db

app = create_app()

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# ルートパスへのアクセスをログインページへリダイレクト
@app.route('/', methods=['GET'])
def top():
    return redirect(url_for('login_view'))

# ログインページ表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')
    # Userテーブルからemailに一致するユーザを取得
    user = User.find_by_email(email)

    if email == '' or password == '':
        flash('空のフォームがあるっタラコ！')
    elif user == None:
        flash('Eメールアドレスか、パスワーを間違っタラコ？')
    elif check_password_hash(user.password, password) == False:
        flash('Eメールアドレスか、パスワーをsが間違っタラコ？')
    else:
        login_user(user)
        user_name = user.user_name
        flash('おかえり！ ' + user_name + 'さん！')
        return redirect(url_for('chats_view'))
    return render_template('login.html')
            

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしタラコ！')
    return redirect(url_for('login_view'))


@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_process():
    new_uname = request.form.get('user_name')
    new_email = request.form.get('email')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation') 
    registered_email= User.find_by_email(new_email)
    registered_name = User.find_by_uname(new_uname)

    if new_uname == '' or new_email =='' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるっタラコ！')
    elif password != passwordConfirmation:
        flash('パスワードが一致しないっタラコ！')
    elif registered_name != None:
        flash('ごめんたいm(_ _)m このユーザ名は既に登録されタラコ...')  
    elif registered_email != None:
        flash('ごめんたいm(_ _)m このEメールアドレスは既に登録されタラコ...')
    else:
        User.regist(new_uname, new_email, password)
        flash( 'ようこそ！ ' + new_uname + 'さん！')
        return redirect(url_for('chats_view'))
    return render_template('register.html')
    
@app.route('/chats', methods=['GET'])
@login_required
def chats_view():
    chats = Chat.query.all()
    return render_template('chats.html', chats=chats)

# チャット作成画面遷移
@app.route('/chat/create', methods=['GET'])
@login_required
def chat_create_view():
    return render_template('chatsCreate.html')

# チャットルーム作成
@app.route('/chat/create', methods=['POST'])
@login_required
def create_chat():
    new_chat_name = request.form.get('chat_name')
    if new_chat_name == '':
        return redirect(url_for('chat_create_view'))
    chat_exist = Chat.find_by_name(new_chat_name)

    if chat_exist == None:
        chat_id = uuid.uuid4()
        user_id = current_user.get_id()
        chat_detail = request.form.get('detail')
        # TODO: 追加機能用 chat_type = request.form.get('chat_type')
        Chat.create(chat_id, user_id, new_chat_name, chat_detail)
        return redirect(url_for('chats_view'))
    else:
        error = 'すでに同じ名前のチャンネルが存在しています'
        return render_template('chatsCreate.html', error=error)

# チャットへ遷移
@app.route('/chat/<chat_id>/messages', methods=['GET'])
@login_required
def messages_view(chat_id):
    chat_room = Chat.find_by_chat_info(chat_id)
    messages = Message.get_messages(chat_id)

    return render_template('messages.html', chat=chat_room, messages=messages)

# メッセージ作成
@app.route('/chat/<chat_id>/messages', methods=['POST'])
@login_required
def create_message(chat_id):
    message = request.form.get('message')
    id = uuid.uuid4()
    user_id = current_user.get_id() # TODO:session.get('id')では行かない理由を調べる・聞く
    # TODO: 追加機能・メッセージではなくスタンプの場合用
    if message:
        Message.create(id, user_id, chat_id, message)
    return redirect(f'/chat/{chat_id}/messages')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)