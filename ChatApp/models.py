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
    members = db.relationship('Member', backref='users')

    def get_id(self):
        return self.user_id
    
    @classmethod
    def get_user_id_by_user_name(cls, user_name):
        try:
            result = db.session.query(User).filter(User.user_name == user_name).first()
            return result.user_id
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def get_user_name_by_user_id(cls, user_id):
        try:
            result = db.session.query(User).filter(User.user_id == user_id).first()
            return result.user_name
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
    members = db.relationship('Member', backref='chat')

    @classmethod
    def create(cls, chat_id, user_id, chat_name, chat_type, detail):
        now = datetime.datetime.now()
        chat_new = Chat(id=chat_id, user_id=user_id, chat_name=chat_name, chat_type=chat_type, detail=detail, created_at=now, update_at=now, latest_messages=now)
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
            return {"id": result.id, "user_id": result.user_id, "chat_name": result.chat_name, "detail": result.detail, 'chat_type': result.chat_type}
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def search_chat_exist(cls, user_id, friend_id, user_name, friend_name):
        try:
            result1 = db.session.query(Chat).filter(Chat.chat_type == 2, Chat.user_id == user_id, Chat.chat_name == friend_name).first()
            result2 = db.session.query(Chat).filter(Chat.chat_type == 2, Chat.user_id == friend_id, Chat.chat_name == user_name).first()
            print('===============')    # TODO: 全部のパターンを確認してから消す
            print(result1, result2)
            if (result1 == None) and (result2 == None):
                return False
            else:
                return True
        except Exception as e:
            print(e)
        finally:
            db.session.close()


    @classmethod
    def get_chat_belong_to(cls, user_id):
        try:
            open_chats = db.session.query(Chat).filter(Chat.chat_type == 0).all()
            group_chats = db.session.query(Chat, Member).join(Chat, Chat.id == Member.chat_id).filter(Chat.chat_type == 1, Member.user_id == user_id).all()
            print('0==============')
            print(open_chats)
            print('1.=============')
            print(group_chats)
            chats = open_chats
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

# Memberテーブル
class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.String(255), nullable=False, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    chat_id = db.Column(db.ForeignKey('chat.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime)

    @classmethod
    def search_in_chat(cls, chat_id, user_id):
        try:
            chat_in = db.session.query(Member).filter(Member.chat_id == chat_id, Member.user_id == user_id).first()
            return chat_in
        except Exception as e:
            print(e)
        finally:
            db.session.close()

    @classmethod
    def add_member(cls, id, chat_id, user_id):
        try:
            now = datetime.datetime.now()
            insert_member = Member(id=id, chat_id=chat_id, user_id=user_id, created_at=now)
            db.session.add(insert_member)
            db.session.commit()
        except Exception as e:
            print(e)
        finally:
            db.session.close()