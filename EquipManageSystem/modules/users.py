import hashlib

from sqlalchemy import MetaData, Table

from app import db


class Users(db.Model):  # 用户表
    __table__ = Table('t_user', MetaData(bind=db.engine), autoload=True)

    def find_user_by_id(self, uid):
        row = db.session.query(Users).filter(Users.uid == uid).first()
        return row

    def find_user_by_uname(self, uname):
        row = db.session.query(Users).filter(Users.username == uname).first()
        return row

    def insert_user(self, uname, password, tel, isout=1):
        m = hashlib.md5()  # 加密
        m.update(password.encode("utf8"))
        user = Users(username=uname, password=m.hexdigest(), tel=tel, is_out=isout)
        db.session.add(user)
        db.session.commit()
