from sqlalchemy import Table, MetaData

from app import db


class Equipment(db.Model):  # 器材表
    __table__ = Table('t_equipment', MetaData(bind=db.engine), autoload=True)

    # 按编号找
    def find_eqp_by_id(self, eqpid):
        row = db.session.query(Equipment).filter(Equipment.eqpid == eqpid).first()
        return row

    # 显示所有器材
    def show_eqp_all(self):
        row = db.session.query(Equipment).filter().all()
        return row

    # 按器材名找
    def find_eqp_by_name(self, name):
        row = db.session.query(Equipment).filter(Equipment.eqp_name == name).first()
        return row

    # 新增器材
    def insert_eqp(self, eqp_name,num):
        neweqp = Equipment(eqp_name=eqp_name,num=num)
        db.session.add(neweqp)
        db.session.commit()

    # 按对象修改
    def update_addr(self, eqp):
        self.eqp_name = eqp.eqp_name
        self.num=eqp.num
        db.session.commit()

     # 删除
    def delete(self, id):
        row =Equipment().find_eqp_by_id(id)
        db.session.delete(row)
        db.session.commit()