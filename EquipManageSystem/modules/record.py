from datetime import datetime

from sqlalchemy import MetaData, Table, null

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

    # 添加
    def insert_rec(self, bid,admid,rtn_date,is_return,remark):
        n = Record(bid=bid, admid=admid,rtn_date=datetime.strptime(rtn_date, '%Y-%m-%d').date(),
                    is_return=is_return,remark=remark)
        db.session.add(n)
        db.session.commit()

    # 修改日期和状态
    def update_rec(self,date,is_return):
        self.rtn_date=date
        self.is_return=is_return
        db.session.commit()

