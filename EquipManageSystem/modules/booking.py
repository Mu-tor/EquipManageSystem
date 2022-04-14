from datetime import datetime

from sqlalchemy import MetaData, Table, null

from app import db
from modules.brodtl import Brodtl
from modules.users import Users
from modules.work import Work


class Booking(db.Model):  # 预约表
    __table__ = Table('t_booking', MetaData(bind=db.engine), autoload=True)

    def find_book_by_bid(self, bid):
        row = db.session.query(Booking).filter(Booking.bid == bid).first()
        return row

    def find_all_by_uid(self, uid):
        row = db.session.query(Booking).filter(Booking.uid == uid).all()
        return row

    def find_waitreturn_by_uid(self, uid):  # 查询用户待还
        row = self.find_all_by_uid(uid)

    def find_all_by_username(self, username):  # 通过用户名查询借用的记录
        row = db.session.query(Booking, Users, Brodtl).join(Users, Users.uid == Booking.uid). \
            join(Brodtl, Brodtl.bid == Booking.bid).filter(
            Users.username == username).all()
        return row

    def find_all_by_isagree_uid(self, is_agree, uid):  # 查询用户是否被同意借用的记录
        row = db.session.query(Booking).filter(Booking.is_agree == is_agree, Booking.uid == uid).all()
        return row

    def find_all_by_isagree(self, is_agree):  # 查询所有是否被同意借用的记录
        row = db.session.query(Booking).filter(Booking.is_agree == is_agree).all()
        return row

    # 查询所有预约
    def find_all(self):
        row = db.session.query(Booking).all()
        return row

    # 查询当前场地当前时间是否已被借用
    def find_book_by_date_addr(self, date, addrid, is_agree=1):
        # 为 None即为可借,不为None即为不可同意
        row = db.session.query(Booking, Brodtl).join(Brodtl, Brodtl.bid == Booking.bid).filter(
            Booking.bro_time == date, Brodtl.addrid == addrid,
            Booking.is_agree == is_agree).first()
        return row

    # 添加
    def insert_book(self, uid, bro_time, days=1, is_agree=-1):
        book = Booking(uid=uid, bro_time=datetime.strptime(bro_time, '%Y-%m-%d'),
                       days=days, is_agree=is_agree)
        db.session.add(book)
        db.session.commit()
        return book

    # 修改
    def update_book(self, notc):
        self.uid = notc.uid
        self.bro_time = notc.bro_time
        self.days = notc.days
        self.is_agree = notc.is_agree
        db.session.commit()

    # 按预约编号取消预约
    def cancel(self, id):
        row = Booking().find_book_by_bid(id)
        row.is_agree = -2
        db.session.add(row)
        w = Work().find_work_by_bid(id)
        w.is_deal = 1
        db.session.commit()
