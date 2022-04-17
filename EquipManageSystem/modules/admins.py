import hashlib

from sqlalchemy import MetaData, Table

from app import db


class Admins(db.Model):  # 管理员表
    __table__ = Table('t_admin', MetaData(bind=db.engine), autoload=True)

    def find_admin_by_id(self, admid):
        row = db.session.query(Admins).filter(Admins.admid == admid).first()
        db.session.close()
        return row

    def find_admin_by_admnane(self, admname):
        row = db.session.query(Admins).filter(Admins.admname == admname).first()
        db.session.close()
        return row

    def update_adm(self, user):
        self.admname = user.admname
        self.password = user.password
        db.session.commit()
        db.session.close()

    # 删除
    def delete(self, id):
        row = Admins().find_adm_by_id(id)
        db.session.delete(row)
        db.session.commit()
        db.session.close()

    def insert_admin(self, uname, password):
        m = hashlib.md5()  # 加密
        m.update(password.encode("utf8"))
        admin = Admins(admname=uname, password=m.hexdigest())
        db.session.add(admin)
        db.session.commit()
        db.session.close()
