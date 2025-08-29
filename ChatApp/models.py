# from sqlalchemy import Column, String, Integer, DateTime, update
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid
from __init__ import db
from flask import abort
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()

# Userテーブル
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    # ユーザーIDの取得
    def get_id(self):
        return self.id
    
    @classmethod
    def get_user_by_user_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT * FROM users WHERE id = %s'
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
        
    
    @classmethod
    def get_user_id_by_user_name(cls, user_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT id FROM users WHERE user_name = %s'
                cur.execute(sql, (user_name,))
                user_query = cur.fetchall()
                if user_query:
                    user_id = user_query[0]['id']
                    return user_id
                return user_query
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_user_name_by_user_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT user_name from users WHERE id = %s'
                cur.execute(sql, (user_id,))
                user_query = cur.fetchall()
                if user_query:
                    user_name = user_query[0]['user_name']
                    return user_name
                return user_query
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ユーザ登録
    @classmethod
    def regist(cls, user_id, user_name, email, password, icon_img, created_at):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (id, user_name, email, password, icon_img, created_at) VALUES (%s, %s, %s, %s, %s, %s);"
                cur.execute(sql, (user_id, user_name, email, password, icon_img, created_at,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            login_user(User(user_id))
            db_pool.release(conn)

    # ユーザ情報削除
    @classmethod
    def delete_user(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'DELETE FROM users WHERE id = %s'
                cur.execute(sql, (user_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ユーザ名変更
    @classmethod
    def change_uname(cls, user_name, updated_at, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET user_name=%s, updated_at=%s WHERE id=%s;"
                cur.execute(sql, (user_name, updated_at, user_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # Eメールアドレス変更
    @classmethod
    def change_email(cls, email, updated_at, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET email=%s, updated_at=%s WHERE id=%s;"
                cur.execute(sql, (email, updated_at, user_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # パスワード変更
    @classmethod
    def change_password(cls, password, updated_at,  user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET password=%s, updated_at=%s WHERE id=%s;"
                cur.execute(sql, (password, updated_at, user_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ユーザアイコン変更
    @classmethod
    def change_icon(cls, icon_img, updated_at, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE users SET icon_img=%s, updated_at=%s WHERE id=%s;"
                cur.execute(sql, (icon_img, updated_at, user_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    # 登録済みEメールアドレスの確認
    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # 登録済みユーザ名の確認
    @classmethod
    def find_by_uname(cls, name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE user_name=%s;"
                cur.execute(sql, (name,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# Chatテーブル
class Chat():
    @classmethod
    def create(cls, chat_id, user_id, chat_name, chat_type, detail, now):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'INSERT INTO chats(id, user_id, chat_name, chat_type, detail, created_at, updated_at) VALUE(%s, %s, %s, %s, %s, %s, %s)'
                cur.execute(sql, (chat_id, user_id, chat_name, chat_type, detail, now, now,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update_name(cls, chat_id, now, new_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'UPDATE chats SET chat_name = %s, updated_at = %s WHERE id = %s'
                cur.execute(sql, (new_name, now, chat_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update_detail(cls, chat_id, now, new_detail):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'UPDATE chats SET detail = %s, updated_at = %s WHERE id = %s'
                cur.execute(sql, (new_detail, now, chat_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, chat_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'DELETE FROM chats WHERE id = %s'
                cur.execute(sql, (chat_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_name(cls, reserch_chat_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT id FROM chats WHERE chat_name = %s'
                cur.execute(sql, (reserch_chat_name,))
                chat_id = cur.fetchone()
                return chat_id
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_chat_info(cls, reserch_chat_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT * FROM chats WHERE id = %s'
                cur.execute(sql, (reserch_chat_id,))
                chat_info = cur.fetchone()
                return chat_info
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def search_private_chat_exist(cls, user_id, friend_id, user_name, friend_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT id FROM chats WHERE (chat_type = 2) and (user_id = %s) and (chat_name = %s)'
                cur.execute(sql, (user_id, f'{friend_name}・{user_name}',))
                result1 = cur.fetchone()
                cur.execute(sql, (friend_id, f'{user_name}・{friend_name}',))
                result2 = cur.fetchone()
                if (result1 == None) and (result2 == None):
                    return None
                else:
                    return True
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_chat_belong_to(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                chats = []

                open_sql = 'SELECT * FROM chats WHERE chat_type = 0'
                cur.execute(open_sql)
                open_chats = cur.fetchall()

                group_private_sql = '''
                    SELECT c.id, c.user_id, c.chat_name, c.detail, c.chat_type, c.created_at, c.updated_at FROM chats AS c
                    LEFT OUTER JOIN members AS m ON c.id = m.chat_id
                    WHERE (c.chat_type = %s) and (m.user_id = %s);
                    '''
                cur.execute(group_private_sql, (1, user_id))
                group_chats = cur.fetchall()
                cur.execute(group_private_sql, (2, user_id))
                private_chats = cur.fetchall()
                if (not group_chats) and (not private_chats):
                    chats = open_chats
                elif not group_chats:
                    chats = open_chats + private_chats
                elif not private_chats:
                    chats = open_chats + group_chats
                else:
                    chats = open_chats + group_chats + private_chats
                return chats
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


# Messageテーブル
class Message():
    @classmethod
    def create(cls, id, user_id, chat_id, message, now):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'INSERT INTO messages(id, user_id, chat_id, message, created_at) VALUES(%s, %s, %s, %s, %s)'
                cur.execute(sql, (id, user_id, chat_id, message, now,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def send_stamp(cls, id, user_id, chat_id, stamp_id, now):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'INSERT INTO messages(id, user_id, chat_id, stamp_id, created_at) VALUES(%s, %s, %s, %s, %s)'
                cur.execute(sql, (id, user_id, chat_id, stamp_id, now,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'DELETE FROM messages WHERE id=%s'
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_messages(cls, chat_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = '''
                    SELECT m.id, m.user_id, m.message, m.created_at, s.title, s.stamp_path, u.user_name, u.icon_img
                    FROM messages AS m
                    LEFT OUTER JOIN stamps AS s ON m.stamp_id = s.id
                    LEFT OUTER JOIN users AS u ON m.user_id = u.id
                    WHERE chat_id = %s
                    ORDER BY m.created_at ASC;
                    '''
                cur.execute(sql, (chat_id,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_latest_messages(cls, chat_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT created_at FROM messages WHERE chat_id = %s ORDER BY created_at DESC LIMIT 1;'
                cur.execute(sql, (chat_id,))
                latest_message = cur.fetchone()
                if latest_message == None:
                    return None
                return latest_message['created_at']
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


# Memberテーブル
class Member():
    @classmethod
    def search_in_chat(cls, chat_id, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT * FROM members AS m WHERE (m.chat_id = %s) and (m.user_id = %s)'
                cur.execute(sql, (chat_id, user_id,))
                chat_in = cur.fetchall()
                return chat_in
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def add_member(cls, id, chat_id, user_id, now):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'INSERT INTO members(id, chat_id, user_id, created_at) VALUE(%s, %s, %s, %s)'
                cur.execute(sql, (id, chat_id, user_id, now,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_chat_member(cls, chat_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT * FROM members WHERE chat_id = %s'
                cur.execute(sql, (chat_id,))
                members = cur.fetchall()
                return members
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


# Stampテーブル
class Stamp():
    @classmethod
    def get_stamps(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT * FROM stamps'
                cur.execute(sql)
                stamps = cur.fetchall()
                return stamps
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)