from datetime import datetime

from sqlalchemy import MetaData, Table

from app import db
from modules.booking import Booking
from modules.brodtl import Brodtl
from modules.equipment import Equipment
from modules.users import Users
from modules.work import Work


class Record(db.Model):  # 借用记录表
    __table__ = Table('t_record', MetaData(bind=db.engine), autoload=True)

    def find_rec_by_bid(self, bid):
        row = db.session.query(Record).filter(Record.bid == bid).first()
        return row

    def find_all_by_admid(self, admid):
        row = db.session.query(Record).filter(Record.admid == admid).all()
        return row

    def find_all_by_isrtn(self, isrtn, uid):  # 查询用户归还状态
        row = db.session.query(Record, Booking).join(Booking, Booking.bid == Record.bid) \
            .join(Users, Users.uid == Booking.uid).filter(Users.uid == uid, Record.is_return == isrtn).all()
        return row

    # 查询所有归还记录
    def find_all(self):
        row = db.session.query(Record).all()
        return row

    # 管理员同意及驳回预约，添加至预约详情表,并将待处理事务改为已处理
    def insert_rec(self, bid, admid, remark, is_agree, is_return=0):
        record = Record(bid=bid, admid=admid, is_return=is_return, remark=remark)
        db.session.add(record)
        bookings = Booking()
        brodtl = Brodtl()
        bro = brodtl.find_book_by_bid(bid)
        if bro.is_addr == 0:  # 修改器材数量
            equip = Equipment()
            eq = equip.find_eqp_by_id(bro.eqpid)
            eq.update_eqp(eq.eqp_name, eq.num - bro.bro_num)
        book = bookings.find_book_by_bid(bid)
        book.is_agree = is_agree
        bookings.update_book(book)
        work = Work()
        row = work.find_work_by_bid(bid)
        row.is_deal = 1  # 将待处理事务改为已处理
        db.session.add(row)
        db.session.commit()

    # 修改日期和状态
    def update_rec(self, bid, remark, date, is_return=1):
        rec = self.find_rec_by_bid(bid)
        rec.rtn_date = datetime.strptime(date, '%Y-%m-%d')
        rec.remark = remark
        rec.is_return = is_return
        db.session.add(rec)
        db.session.commit()
