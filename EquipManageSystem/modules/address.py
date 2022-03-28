from sqlalchemy import Table, MetaData

from app import db


class Address(db.Model):  # 场地表
    __table__ = Table('t_addr', MetaData(bind=db.engine), autoload=True)

    # 按编号找
    def find_addr_by_id(self, addrid):
        row = db.session.query(Address).filter(Address.addrid == addrid).first()
        return row

    # 按场地名找
    def find_addr_by_addr(self, address):
        row = db.session.query(Address).filter(Address.address == address).first()
        return row

    # 新增场地
    def insert_addr(self, address):
        newaddr = Address(address=address)
        db.session.add(newaddr)
        db.session.commit()

    # 按对象修改
    def update_addr(self, addr):
        self.address = addr.address
        db.session.commit()

     # 删除
    def delete(self, id):
        row = Address().find_addr_by_id(id)
        db.session.delete(row)
        db.session.commit()