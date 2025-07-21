from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin):
    user_id = db.Column(db.String(255), primary_key=True)
    user_name = db.Column(db.String(255),  nullable=False)
    email = db.Column(db.String(255), unique=True, nullabel=False)
    password_hash = db.Column(db.String(255), nullable=False)
    icon_img = db.Column(db.String(255))
    # company_id = db.Column(db.Integer, db.schema.ForeignKey("companies.id", name="?????", nullable=False))
    # nickname = db.Column(db.String(255))
    created_at = db.Column(db.Datetime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
