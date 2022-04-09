from datetime import datetime

from sqlalchemy import MetaData, Table, null

from app import db
from modules.work import Work


class Brodtl(db.Model):  # 预约详情表
    __table__ = Table('t_brodtl', MetaData(bind=db.engine), autoload=True)

    def find_book_by_bid(self, bid):
        row = db.session.query(Brodtl).filter(Brodtl.bid == bid).first()
        return row

    def find_all_by_eqpid(self, eqpid):
        row = db.session.query(Brodtl).filter(Brodtl.eqpid == eqpid).all()
        return row

    def find_all_by_isaddr(self, is_addr):
        row = db.session.query(Brodtl).filter(Brodtl.is_addr == is_addr).all()
        return row

    # 查询所有预约
    def find_all(self):
        row = db.session.query(Brodtl).all();
        return row

    # 添加
    def insert_bro(self, bid, eqpid, addrid, is_addr, bro_num):
        n = Brodtl(bid=bid, eqpid=eqpid, addrid=addrid, is_addr=is_addr, bro_num=bro_num)
        db.session.add(n)
        db.session.commit()

    # 修改
    def update_bro(self, bro):
        self.bid = bro.bid
        self.eqpid = bro.eqpid
        self.addrid = bro.addrid
        self.is_addr = bro.is_addr
        self.bro_num = bro.bro_num
        db.session.commit()
