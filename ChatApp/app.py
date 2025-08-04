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

@app.route('/', methods=['GET'])
def top():
    return redirect(url_for('login_view'))

@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')
    # Userテーブルからemailに一致するユーザを取得
    user = User.query.filter_by(email=email).first()
    # user_id = user.user_id
    if user == None:
        flash('Eメールアドレスまたはパスワードが間違っています。')
        return render_template('login.html')
    else:
        if check_password_hash(user.password, password):
            login_user(user)
            user_name = user.user_name
            #user_id = user.user_id
            flash('おかえりなさい！ ' + user_name + 'さん！')
            return redirect(url_for('chats_view'))
        else:
            flash('Eメールアドレスまたはパスワードが間違っています。')
            return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return render_template('login.html')


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
        flash('このEメールアドレスは既に使用されています。別のEメールアドレスで登録してください。')
    elif registered_name != None:
        flash('このユーザは既に使用されています。別のユーザ名で登録してください。')
    elif user_name == '' or email =='' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるようです。')
    elif password != passwordConfirmation:
        flash('パスワードが一致しません。')
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
        flash( 'ようこそ！ ' + user_name + 'さん！')
        return redirect(url_for('chats_view'))
    return render_template('register.html')
    
@app.route('/chats', methods=['GET'])
@login_required
def chats_view():
    chats = Chat.query.all()
    # chats = Chat.query.filter_by(Chat.user_id == current_user.get_id()).order_by(Chat.created_at).all()
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

# チャット編集画面
@app.route('/chat/<chat_id>/detail', methods=['GET'])
@login_required
def chat_detail(chat_id):
    chat_room = Chat.find_by_chat_info(chat_id)
    return render_template('chatsUpdate.html', chat=chat_room)

# チャット更新
@app.route('/chat/update/<chat_id>', methods=['POST'])
@login_required
def update_chat(chat_id):
    user_id = current_user.get_id()
    new_name = request.form.get('chat_name')
    new_detail = request.form.get('detail')
    chat_info = Chat.find_by_chat_info(chat_id)
    if chat_info['user_id'] != user_id:
        error = '他の人が作ったチャンネルです'
        return render_template('ChatsUpdate.html', chat=chat_info, error=error)
    elif (new_name == "") and (new_detail == ""):
        return render_template('ChatsUpdate.html', chat=chat_info)
    elif chat_info != None:
        Chat.update(chat_id, new_name, new_detail)
        message = 'チャット情報が更新されました！'
    return render_template('ChatsUpdate.html', chat=chat_info, message=message)

# チャット削除
@app.route('/chat/delete/<chat_id>', methods=['POST'])
@login_required
def delete_chat(chat_id):
    user_id = current_user.get_id()
    chat_info = Chat.find_by_chat_info(chat_id)
    if chat_info['user_id'] != user_id:
        error = '他の人が作ったチャンネルです'
        return render_template('ChatsUpdate.html', chat=chat_info, error=error)
    elif chat_info != None:
        Chat.delete(chat_id)
    return redirect(url_for('chats_view'))

# チャットへ遷移
@app.route('/chat/<chat_id>/messages', methods=['GET'])
@login_required
def messages_view(chat_id):
    user_id = current_user.get_id()
    chat_room = Chat.find_by_chat_info(chat_id)
    messages = Message.get_messages(chat_id)

    return render_template('messages.html', user_id=user_id, chat=chat_room, messages=messages)

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

# メッセージ削除
@app.route('/chat/<chat_id>/messages/<message_id>', methods=['POST'])
@login_required
def delete_message(chat_id, message_id):

    if message_id:
        Message.delete(message_id)

    return redirect(f'/chat/{chat_id}/messages')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)