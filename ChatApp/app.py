from flask import Flask, render_template, request, session
import uuid
from __init__ import create_app
from models import Chat, Message

app = create_app()
# TODO:flask_loginを実装したらログイン状態でのみアクセスできるようにデコレータ
@app.route('/chat')
def home():
    return render_template('chats.html')

# チャットルーム作成
@app.route('/chat', methods=['POST'])
def create_chat():
    new_chat_name = request.form.get('chat_name')
    chat_exist = Chat.find_by_name(new_chat_name)

    if chat_exist == None:
        chat_id = uuid.uuid4()
        # TODO: ログイン機能が実装された後に修正
        user_id = 'test'# session.get('user_id')
        chat_detail = request.form.get('detail')
        # 追加機能用
        # chat_type = request.form.get('chat_type')
        Chat.create(chat_id, user_id, new_chat_name, chat_detail)
        # TODO: 実装によって、リダイレクト先を変更
        return render_template('chat.html')
    else:
        error = 'すでに同じ名前のチャンネルが存在しています'
        # TODO: エラー時にどう対応するかによって変更
        return error

# チャットへ遷移
@app.route('/chat/<chat_id>/messages', methods=['GET'])
def open_chat(chat_id):
    chat_room = Chat.find_by_chat_info(chat_id)
    messages = Message.get_messages(chat_id)

    # TODO:user_idも返す
    return render_template('messages.html', chat=chat_room, messages=messages)

# メッセージ作成
@app.route('/chat/<chat_id>/messages', methods=['POST'])
def create_message(chat_id):
    # メッセージ受け取り
    message = request.form.get('message')
    id = uuid.uuid4()
    user_id = 'test'
    # データベース登録
    if message:
        Message.create(id, user_id, chat_id, message)
    # 終了
    return 'OK'

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)