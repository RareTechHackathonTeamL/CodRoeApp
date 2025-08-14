from sqlalchemy import Column, String, Integer, DateTime, update
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid
from __init__ import db

# Userテーブル
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(255), primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # icon_img = db.Column(db.String(255))
    # company_id = db.Column(db.Integer, db.schema.ForeignKey("companies.id", name="?????", nullable=False))
    # nickname = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime)  # 更新日時

    chat = db.relationship('Chat', backref='users')
    messages = db.relationship('Message', backref='users')

    # ユーザーIDの取得
    def get_id(self):
        return self.user_id

    # ユーザ登録
    @classmethod
    def regist(cls, user_name, email, password):
        user_id=uuid.uuid4()
        now = datetime.datetime.now()
        password = generate_password_hash(password)
        new_user = User(user_id=user_id, user_name=user_name, email=email, password=password, created_at=now)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            login_user(new_user)
            db.session.close()

    # ユーザ情報更新(パスワード更新なし)
    @classmethod
    def update_nopass(cls, user_id, user_name, email):
        user = db.session.query(User).filter(User.user_id == user_id).first()
        user.user_name = user_name
        user.email = email
        user.update_at = datetime.datetime.now()
        try:
            # db.session.merge(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    # ユーザ情報更新(パスワード更新あり)
    @classmethod
    def update_user(cls, user_id, user_name, email, password):
        user = db.session.query(User).filter(User.user_id == user_id).first()
        user.user_name = user_name
        user.email = email
        user.password = generate_password_hash(password)
        user.update_at = datetime.datetime.now()
        try:
            db.session.merge(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    #  ユーザ情報更新(パスワード更新のみ)
    @classmethod
    def update_password(cls, user_id, password):
        user = db.session.query(User).filter(User.user_id == user_id).first()
        user.password = generate_password_hash(password)
        user.update_at = datetime.datetime.now()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    # ユーザ情報削除
    @classmethod
    def delete_user(cls, user_id):
        # user = db.session.query(User).filter(User.user_id == user_id).first()
        # now = datetime.datetime.now()
        try:
            # with db.session.begin(subtransactions=True):
            db.session.query(User).filter(User.user_id == user_id).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            # db.session.rollback()
            # raise
        finally:
            db.session.close()
    
    # 登録済みEメールアドレスの確認
    @classmethod
    def find_by_email(cls, reserch_email):
        try:
            result = db.session.query(User).filter(User.email == reserch_email).first()
            return result
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    # 登録済みユーザ名の確認
    @classmethod
    def find_by_uname(cls, reserch_name):
        try:
            result = db.session.query(User).filter(User.user_name == reserch_name).first()
            return result
        except Exception as e:
            print(e)
        finally:
            db.session.close()  


# Chatテーブル
class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.String(255), nullable=False, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    chat_name = db.Column(db.String(255), nullable=False)
    chat_type = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime)
    latest_messages = db.Column(db.DateTime, nullable=False)    # チャット一覧で最新のメッセージが来ているものを上に表示させたいため、新規メッセージ・チャット新規作成のみでupdateする

    messages = db.relationship('Message', backref='chat')

    @classmethod
    def create(cls, chat_id, user_id, chat_name, detail):
        now = datetime.datetime.now()
        chat_new = Chat(id=chat_id, user_id=user_id, chat_name=chat_name, chat_type=1, detail=detail, created_at=now, update_at=now, latest_messages=now)
        try:
            db.session.add(chat_new)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    @classmethod
    def update(cls, chat_id, new_name, new_detail):
        try:
            chat_info = db.session.query(Chat).filter(Chat.id == chat_id).first()
            if new_name != '':
                chat_info.chat_name = new_name
            if new_detail != '':
                chat_info.detail = new_detail
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    @classmethod
    def update_latest(cls, chat_id):
        try:
            now = datetime.datetime.now()
            chat_info = db.session.query(Chat).filter(Chat.id == chat_id).first()
            chat_info.latest_messages = now
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    @classmethod
    def delete(cls, chat_id):
        try:
            db.session.query(Chat).filter(Chat.id == chat_id).delete()
            db.session.commit()
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def find_by_name(cls, reserch_chat_name):
        try:
            result = db.session.query(Chat).filter(Chat.chat_name == reserch_chat_name).first()
            return result
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def find_by_chat_info(cls, reserch_chat_id):
        try:
            result = db.session.query(Chat).filter(Chat.id == reserch_chat_id).first()
            return {"id": result.id, "user_id": result.user_id, "chat_name": result.chat_name, "detail": result.detail}
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def get_chat_latest(cls):
        try:
            chats = db.session.query(Chat).order_by(Chat.latest_messages.desc()).all()
            return chats
        except Exception as e:
            print(e)
        finally:
            db.session.close()


# Messageテーブル
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(255), nullable=False, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    chat_id = db.Column(db.String(255), db.ForeignKey('chat.id'), nullable=False)
    message = db.Column(db.Text)
    # stamp_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime)

    @classmethod
    def create(cls, id, uid, cid, message):
        now = datetime.datetime.now()
        insert_message = Message(id=id, user_id=uid, chat_id=cid, message=message, created_at=now)
        try:
            db.session.add(insert_message)
            db.session.commit()
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def delete(cls, message_id):
        try:
            db.session.query(Message).filter(Message.id==message_id).delete()
            db.session.commit()
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def get_messages(cls, cid):
        try:
            messages = db.session.query(Message).filter(Message.chat_id == cid).order_by(Message.created_at).all()
            result = [{
                'id': m.id,
                'user_id': m.user_id,
                'message': m.message,
                'created_at': m.created_at,
                } for m in messages]
            return result
        except Exception as e:
            print(e)
        finally:
            db.session.close()  # TODO: flask_sqlalchemyでは必要ないというものを見た（公式ドキュメントには書いていない）必要か聞く