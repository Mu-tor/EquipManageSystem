from sqlalchemy import MetaData, Table

from app import db


class Work(db.Model):  # 事务表
    __table__ = Table('t_work', MetaData(bind=db.engine), autoload=True)

    def find_work_by_wid(self, wid):
        row = db.session.query(Work).filter(Work.wid == wid).first()
        return row

    # 按处理状态查找
    def find_all_by_isdeal(self, isdeal):
        row = db.session.query(Work).filter(Work.is_deal == isdeal).all()
        return row

    # 按预约id查找
    def find_work_by_bid(self, bid):
        row = db.session.query(Work).filter(Work.bid == bid).first()
        return row

    # 查询所有事务
    def find_all(self):
        row = db.session.query(Work).all();
        return row

