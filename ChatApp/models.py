from sqlalchemy import Column, String, Integer, DateTime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from __init__ import db


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

    def get_id(self):
        return self.user_id  



# Chatテーブル
class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.String(255), nullable=False, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False)
    chat_name = db.Column(db.String(255), nullable=False)
    chat_type = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    messages = db.relationship('Message', backref='chat')

    @classmethod
    def create(cls, chat_id, user_id, chat_name, detail):
        now = datetime.datetime.now()
        chat_new = Chat(id=chat_id, user_id=user_id, chat_name=chat_name, chat_type=1, detail=detail, created_at=now, update_at=now)
        try:
            db.session.add(chat_new)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
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
            return {"id": result.id, "chat_name": result.chat_name, "detail": result.detail}
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
    def get_messages(cls, cid):
        try:
            messages = db.session.query(Message).filter(Message.chat_id == cid).all()
            result = [{
                'message': m.message,
                'created_at': m.created_at,
                } for m in messages]
            return result
        except Exception as e:
            print(e)
        finally:
            db.session.close()  # TODO: flask_sqlalchemyでは必要ないというものを見た（公式ドキュメントには書いていない）必要か聞く