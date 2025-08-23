from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Chat, Message, Member, Stamp
import uuid
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
        flash('おかえり！ ' + user_name + 'さん！' + str(user_id))
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
    # icon_img = '../' + app.config['ICON_FOLDER'] + 'default_image.png'
    icon_img = 'default_image.png'

    if new_uname == '' or new_email =='' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるっタラコ！')
    elif password != passwordConfirmation:
        flash('パスワードが一致しないっタラコ！')
    elif registered_name != None:
        flash('ごめんたい! このユーザ名は既に登録されタラコ...')  
    elif registered_email != None:
        flash('ごめんたい! このEメールアドレスは既に登録されタラコ...')
    else:
        User.regist(new_uname, new_email, password, icon_img)
        user = User.find_by_email(new_email)
        login_user(user)
        session['user_id'] = user.user_id
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
    icon_img = user.icon_img
    icon_img = '../' + app.config['ICON_FOLDER'] + str(user.icon_img)
    return render_template('profile.html', icon_img=icon_img)

# ユーザ名変更画面表示 *****************************************************
@app.route('/change_uname', methods=['GET'])
@login_required
def change_uname_view():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
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
    icon_img = user.icon_img
    icon_img = app.config['ICON_FOLDER'] + str(user.icon_img)
    flash('user_id= ' + str(user_id))
    return render_template('change_icon.html', icon_img=icon_img)

# アイコン変更処理 *****************************************************
@app.route('/change_icon', methods=['POST'])
@login_required
def change_icon():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    file = request.files['icon_file']
    origin_filename = file.filename

    if 'icon_file' not in request.files:
        flash('ファイルが選択されていません！')
    elif origin_filename == '':
        flash('ファイル名が無いか新しいファイルが選択されてません！')
    elif file and allowed_file(origin_filename):
        split_fname = origin_filename.rsplit('.', 1)
        file_ext = split_fname[1]
        filename = str(user_id) + '.' + str(file_ext)
        secure_fname = secure_filename(filename)
        file.save(app.config['ICON_FOLDER'] + secure_fname)
        icon_img = filename
        User.change_icon(user_id, icon_img)
        flash( 'アイコン画像を変更しタラコ！' + str(file_ext))
        return redirect(f'/profile')
    else:
        flash('許可されていないファイルファイル形式です！')
    icon_img = app.config['ICON_FOLDER'] + str(user.icon_img)
    return render_template('change_icon.html', icon_img=icon_img)

# チャット一覧表示
@app.route('/chats', methods=['GET'])
@login_required
def chats_view():
    user_id = current_user.get_id()
    chats = Chat.get_chat_belong_to(user_id)
    return render_template('chats.html', chats=chats)

# チャット作成画面遷移
@app.route('/chat/create', methods=['GET'])
@login_required
def chat_create_view():
    return render_template('chatsCreate.html')

# チャットルーム作成    NOTE:フロントエンドで入力フォームを制御してもらい、titleとメンバー追加を分ける
@app.route('/chat/create', methods=['POST'])
@login_required
def create_chat():
    chat_type = request.form.get('chat_type')
    # 個人チャットの場合
    if chat_type == 'private':
        return redirect(f'/chat/create/select_private')

    new_chat_name = request.form.get('chat_name')
    if new_chat_name == '':
        return redirect(url_for('chat_create_view'))

    # オープン・グループチャットの場合
    chat_exist = Chat.find_by_name(new_chat_name)
    if chat_exist != True:
        chat_id = uuid.uuid4()
        user_id = current_user.get_id()
        chat_detail = request.form.get('detail')

        if chat_type == 'open':
            chat_type = 0
            Chat.create(chat_id, user_id, new_chat_name, chat_type, chat_detail)
            return redirect(url_for('chats_view'))
        elif chat_type == 'group':
            chat_type = 1
            Chat.create(chat_id, user_id, new_chat_name, chat_type, chat_detail)
            id = uuid.uuid4()
            Member.add_member(id, chat_id, user_id)
            return redirect(f'/chat/{ chat_id }/add_member')
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

# グループメンバー追加画面遷移
@app.route('/chat/<chat_id>/add_member', methods=['GET'])
@login_required
def chat_add_member_view(chat_id):
    # 自分がこのチャットに入っているかを検索
    user_id = current_user.get_id()
    in_chat = Member.search_in_chat(chat_id, user_id)
    if in_chat == False:
        flash('このチャットにアクセスできません')
        return redirect(url_for('chats_view'))
    chat_room = Chat.find_by_chat_info(chat_id)
    return render_template('chatsAddMember.html', chat=chat_room)

# グループメンバー追加  TODO:複数のメンバーをリストとして受け入れるようにフロントで設定する
@app.route('/chat/<chat_id>/add_member', methods=['POST'])
@login_required
def chat_add_member(chat_id):
    friend_list = request.form.getlist('friends_name')
    results = []
    for friend in friend_list:
        # 追加するメンバーの名前を検索
        friend_id = User.get_user_id_by_user_name(friend)
        if friend_id == None:
            results.append(f'{friend}さんが見つかりませんでした')
        # メンバーがそのチャットに参加しているか検索
        chat_in = Member.search_in_chat(chat_id, friend_id)
        if chat_in != None:
            results.append(f'{friend}さんは既にチャットに参加しています')
        # メンバーDBに追加
        id = uuid.uuid4()
        Member.add_member(id, chat_id, friend_id)
    if results == None:
        flash('メンバー追加できました！')
        return redirect(f'/chat/{chat_id}/messages')
    else:
        # エラーが起こった場合があるときはグループメンバー追加画面に戻る
        for result in results:
            flash(result)
        return redirect(f'/chat/{chat_id}/add_member')

# プライベートメンバー選択画面遷移
@app.route('/chat/create/select_private', methods=['GET'])
@login_required
def chat_select_private_view():
    return render_template('chatsSlelctPrivate.html')

# プライベートメンバー選択
@app.route('/chat/create/select_private', methods=['POST'])
@login_required
def chat_select_private():
    # プライベートするメンバーの名前を検索
    friend_name = request.form.get('friend_name')
    friend_id = User.get_user_id_by_user_name(friend_name)
    if friend_id == None:
        flash('入力された友達が見つかりません')
        return redirect(url_for('chat_select_private'))
    # 自分と相手とのチャットがすでにできていないか検索
    user_id = current_user.get_id()
    user_name = User.get_user_name_by_user_id(user_id)
    if friend_name == user_name:
        flash('友達を入力してください')
        return redirect(url_for('chat_select_private'))
    chat_exist = Chat.search_chat_exist(user_id, friend_id, user_name, friend_name)
    if chat_exist == True:
        flash('入力された友達とのチャットは存在します')
        return redirect(url_for('chat_select_private'))
    # チャットテーブル作成
    chat_id = uuid.uuid4()
    new_chat_name = f'{friend_name}と{user_name}のプライベートチャット'
    chat_type = 2
    chat_detail = ''
    Chat.create(chat_id, user_id, new_chat_name, chat_type, chat_detail)
    # メンバーテーブルに追加
    id = uuid.uuid4()
    Member.add_member(id, chat_id, user_id)
    id = uuid.uuid4()
    Member.add_member(id, chat_id, friend_id)
    # そのチャットに遷移
    return redirect(f'/chat/{chat_id}/messages')

# チャットへ遷移
@app.route('/chat/<chat_id>/messages', methods=['GET'])
@login_required
def messages_view(chat_id):
    user_id = current_user.get_id()
    chat_room = Chat.find_by_chat_info(chat_id)
    messages = Message.get_messages(chat_id)
    # user_icons = User.get_icons()
    stamps = Stamp.get_stamps()
    # return render_template('messages.html', user_id=user_id, chat=chat_room, messages=messages, stamps=stamps, user_icons=user_icons)
    return render_template('messages.html', user_id=user_id, chat=chat_room, messages=messages, stamps=stamps)

# メッセージ作成
@app.route('/chat/<chat_id>/messages', methods=['POST'])
@login_required
def create_message(chat_id):
    message = request.form.get('message')
    stamp = request.form.get('stamp')
    id = uuid.uuid4()
    user_id = current_user.get_id()
    # TODO: 追加機能・メッセージではなくスタンプの場合用
    if message:
        Message.create(id, user_id, chat_id, message)
        Chat.update_latest(chat_id)
    elif stamp:
        Message.send_stamp(id, user_id, chat_id, stamp)
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