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
            if res: return res
        except:
            print('Database error')
        return[]

    def get_stats(self, username):
        try:
            self.__cur.execute(f"SELECT username, best FROM users WHERE username LIKE '{username}'")
            res = self.__cur.fetchall()
            return res
        except: return[]
    
    def get_leaders(self):
        sql = """SELECT username, best FROM users ORDER BY best ASC"""
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
    
    def get_menu(self):
        sql = """SELECT * FROM menu"""
        try: 
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Database error')
        return[]
