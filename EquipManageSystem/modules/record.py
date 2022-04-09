from datetime import datetime

from sqlalchemy import MetaData, Table

from app import db
from modules.work import Work


class Record(db.Model):  # 借用记录表
    __table__ = Table('t_record', MetaData(bind=db.engine), autoload=True)

    def find_rec_by_bid(self, bid):
        row = db.session.query(Record).filter(Record.bid == bid).first()
        return row

    def find_all_by_admid(self, admid):
        row = db.session.query(Record).filter(Record.admid == admid).all()
        return row

    def find_all_by_isrtn(self, isrtn):
        row = db.session.query(Record).filter(Record.is_return == isrtn).all()
        return row

    # 查询所有归还记录
    def find_all(self):
        row = db.session.query(Record).all();
        return row

    # 管理员同意预约，添加至预约表,并将待处理事务改为已处理
    def insert_rec(self, bid, admid, remark, is_return=0):
        record = Record(bid=bid, admid=admid, is_return=is_return, remark=remark)
        db.session.add(record)
        work = Work()
        row = work.find_work_by_bid(bid)
        row.is_deal = 1  # 将待处理事务改为已处理
        db.session.add(row)
        db.session.commit()

    # 修改日期和状态
    def update_rec(self, bid, date, remark, is_return=1):
        rec = self.find_rec_by_bid(bid)
        rec.rtn_date = datetime.strptime(date, '%Y-%m-%d').date()
        rec.remark = remark
        rec.is_return = is_return
        db.session.add(rec)
        db.session.commit()
