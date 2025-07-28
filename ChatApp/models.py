from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

db = SQLAlchemy()

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

    def get_id(self):
        return self.user_id  
    
# Chatテーブル
class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.String(255), nullable=False, primary_key=True)
    # user_id = db.Column(db.String(255), nullable=False)
    chat_name = db.Column(db.String(255), nullable=False)
    chat_type = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime)
    # update_at = db.Column(db.DateTime)