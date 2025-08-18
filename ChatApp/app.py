from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Chat, Message
import pymysql
import uuid, os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from __init__ import create_app, login_manager, db

app = create_app()

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# アップロードファイル形式確認
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        flash('Eメールアドレスか、パスワーを間違っタラコ？')
    else:
        login_user(user)
        user_name = user.user_name
        session['user_id'] = user.user_id
        user_id = session.get('user_id')
        flash('おかえり！ ' + user_name + 'さん！')
        return redirect(url_for('chats_view'))
    return render_template('login.html')
            
# ログアウト処理
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしタラコ！')
    return redirect(url_for('login_view'))

# ユーザ登録画面表示
@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

# ユーザ登録処理
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
        flash('ごめんたい! このユーザ名は既に登録されタラコ...')  
    elif registered_email != None:
        flash('ごめんたい! このEメールアドレスは既に登録されタラコ...')
    else:
        User.regist(new_uname, new_email, password)
        flash( 'ようこそ！ ' + new_uname + 'さん！')
        return redirect(url_for('chats_view'))
    return render_template('register.html')

# ユーザ削除
@app.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    #　GETの場合
    if request.method == 'GET':
        return render_template('delete_user.html', user=user)
    # POSTの場合
    else:
        User.delete_user(user_id)
        flash('ユーザを削除しタラコ！')
        return redirect(url_for('login_view'))
    

# プロフィール画面表示 *****************************************************
@app.route('/profile', methods=['GET'])
@login_required
def profile_view():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user.icon_img = app.config['ICON_FOLDER']+'/'+str(user.icon_img)
    flash('user_id= ' + user_id + ', icon_img= ' + user.icon_img)
    return render_template('profile.html')

# ユーザ名変更画面表示 *****************************************************
@app.route('/change_uname', methods=['GET'])
@login_required
def change_uname_view():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    # flash('user_id= ' + user_id )
    return render_template('change_uname.html')

# ユーザ名変更処理 *****************************************************
@app.route('/change_uname', methods=['POST'])
@login_required
def change_uname():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    current_uname = user.user_name
    new_uname = request.form.get('user_name')

    if new_uname == '' :
        flash('新規情報が入力されていません！')
    elif new_uname == current_uname:
        flash('更新する情報がないっタラコ！')
    else:
        registered_name = User.find_by_uname(new_uname)
        if registered_name != None:
            flash('登録されている情報と一致するため更新できません。')
        else:
            user_name = new_uname
            User.change_uname(user_id, user_name)
            flash('ユーザ情報を更新しタラコ！')
            return redirect(f'/profile')
    return render_template('change_uname.html')

# Eメールアドレス変更画面表示 *****************************************************
@app.route('/change_email', methods=['GET'])
@login_required
def change_email_view():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return render_template('change_email.html')

# Eメールアドレス変更処理 *****************************************************
@app.route('/change_email', methods=['POST'])
@login_required
def change_email():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    current_email = user.email
    new_email = request.form.get('email')

    if new_email == '' :
        flash('新規情報が入力されていません！')
    elif new_email == current_email:
        flash('更新する情報がないっタラコ！')
    else:
        registered_email = User.find_by_email(new_email)
        if registered_email != None:
            flash('登録されている情報と一致するため更新できません。')
        else:
            email = new_email
            User.change_email(user_id, email)
            flash('ユーザ情報を更新しタラコ！')
            return redirect(f'/profile')
    return render_template('change_email.html')

# パスワード変更画面表示 *****************************************************
@app.route('/change_password', methods=['GET'])
@login_required
def change_password_view():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return render_template('change_password.html')

# パスワード変更処理 *****************************************************
@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    current_password = request.form.get('current_password')
    new_password = request.form.get('password')
    new_passwordConfirmation = request.form.get('password-confirmation')

    if current_password == '' or new_password == '' or new_passwordConfirmation == '':
        flash('空のフォームがあります。')
    elif check_password_hash(user.password, current_password) == False:
        flash('現在のパスワードを間違っタラコ？')
    elif new_password != new_passwordConfirmation:
        flash('パスワードが一致しません！')
    else:
        User.change_password(user_id, new_password)
        flash('ユーザ情報を更新しタラコ！')
        return redirect(f'/profile')
    return render_template('change_password.html')

# アイコン変更画面表示 *****************************************************
@app.route('/change_icon', methods=['GET'])
@login_required
def change_icon_view():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    flash('user_id= ' + str(user_id))
    return render_template('change_icon.html')

# アイコン変更処理 *****************************************************
@app.route('/change_icon', methods=['POST'])
@login_required
def change_icon():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    file = request.files['icon_file']
    filetype = request.files['icon_file'].content_type
    origin_filename = file.filename

    if 'icon_file' not in request.files:
        flash('ファイルが選択されていません！')
    elif origin_filename == '':
        flash('ファイル名がありません！')
    elif file and allowed_file(origin_filename):
        secure_fname = secure_filename(origin_filename)
        filename = str(user_id) + '__' + str(secure_fname)
        file.save(os.path.join(app.config['ICON_FOLDER'], filename))
        icon_img = filename
        User.change_icon(user_id, icon_img)
        flash( 'アイコン画像を変更しタラコ！' + str(filetype))
        return redirect(url_for('profile_view'))
    else:
        flash('許可されていないファイルファイル形式です！') 
    return render_template('change_icon.html')

# チャット一覧表示
@app.route('/chats', methods=['GET'])
@login_required
def chats_view():
    chats = Chat.get_chat_latest()
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
        flash('チャット情報が更新されました！')
    return redirect(f'/chat/{ chat_id }/detail')

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
        Chat.update_latest(chat_id)
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