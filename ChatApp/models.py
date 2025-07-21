from sqlalchemy import Column, String, Integer, DateTime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from __init__ import db


# Chatテーブル
class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.String(255), nullable=False, primary_key=True)
    # user_id = db.Column(db.String(255), nullable=False)
    chat_name = db.Column(db.String(255), nullable=False)
    chat_type = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    @classmethod
    def create(cls, chat_id, user_id, chat_name, detail):
        now = datetime.datetime.now()
        chat_a = Chat(id=chat_id, chat_name=chat_name, chat_type=1, detail=detail, created_at=now, update_at=now)
        try:
            with db.session.begin():
                db.session.add(chat_a)
                db.session.commit()
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def find_by_name(cls, reserch_chat_name):
        try:
            with db.session.begin():
                result = db.session.query(Chat).filter(Chat.chat_name == reserch_chat_name).first()
        except Exception as e:
            print(e)
        finally:
            db.session.close()
        return result