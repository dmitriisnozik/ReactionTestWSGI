import sqlite3
from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_all_names(self):
        sql = """SELECT username FROM users"""
        try: 
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Database error')
        return[]

    def get_stats(self, username):
        try:
            self.__cur.execute(f"SELECT username, best FROM users WHERE username LIKE '{username}'")
            res = self.__cur.fetchall()
            return res
        except:
            return[]

    def get_all_users(self):
        try:
            self.__cur.execute("SELECT id, username, best, admin FROM users")
            res = self.__cur.fetchall()
            return res
        except:
            return[]
    
    def get_leaders(self):
        sql = """SELECT username, best FROM users WHERE best NOT NULL ORDER BY best ASC"""
        try: 
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Database error')
        return[]
    
    def add_new(self, user, passw):
        try: 
            self.__cur.execute(f"SELECT COUNT() as count FROM users WHERE username LIKE '{user}'")
            res = self.__cur.fetchone()
            if res['count'] > 0: 
                return False
            self.__cur.execute("""INSERT INTO users VALUES (NULL, ?, ?, NULL, 0)""", (user, passw))
            self.__db.commit()

        except: 
            print('signup error')
            return False
        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('not found')
                return False
            return res
        except:
            return False

    def get_user_by_name(self, username):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE username LIKE '{username}'")
            res = self.__cur.fetchone()
            if not res:
                print('not found')
                return False
            return res
        except: 
            return False
    
    def remove_by_id(self, user_id):
        try:
            self.__cur.execute(f"DELETE FROM users WHERE id = {int(user_id)}")
            self.__db.commit()
        except:
            print('deleting error')

    def remove_by_name(self, username):
        try:
            self.__cur.execute(f"DELETE FROM users WHERE username LIKE '{username}'")
            self.__db.commit()
        except:
            print('deleting error')

    def change_name_by_name(self, username, new):
        try:
            self.__cur.execute(f"UPDATE users SET username='{new}' WHERE username LIKE '{username}'")
            self.__db.commit()
        except:
            print('changing error')

    def change_name_by_id(self, user_id, new):
        try:
            self.__cur.execute(f"UPDATE users SET username='{new}' WHERE id = {user_id}")
            self.__db.commit()
        except:
            print('changing error')

    def change_password_by_name(self, username, new):
        try:
            self.__cur.execute(f"UPDATE users SET password='{new}' WHERE username LIKE '{username}'")
            self.__db.commit()
        except:
            print('changing error')

    def change_password_by_id(self, user_id, new):
        try:
            self.__cur.execute(f"UPDATE users SET password='{new}' WHERE id = {user_id}")
            self.__db.commit()
        except:
            print('changing error')

    def change_result_by_name(self, username, new):
        try:
            self.__cur.execute(f"UPDATE users SET best='{new}' WHERE username LIKE '{username}'")
            self.__db.commit()
        except:
            print('changing error')

    def change_result_by_id(self, user_id, new):
        try:
            self.__cur.execute(f"UPDATE users SET best='{new}' WHERE id = {user_id}")
            self.__db.commit()
        except:
            print('changing error')
        
    def op_by_name(self, username, new):
        try:
            self.__cur.execute(f"UPDATE users SET admin='{new}' WHERE username LIKE '{username}'")
            self.__db.commit()
        except:
            print('changing error')

    def op_by_id(self, user_id, new):
        try:
            self.__cur.execute(f"UPDATE users SET admin='{new}' WHERE id = {user_id}")
            self.__db.commit()
        except:
            print('changing error')
    
    def get_menu(self):
        sql = """SELECT * FROM menu"""
        try: 
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Database error')
        return[]
