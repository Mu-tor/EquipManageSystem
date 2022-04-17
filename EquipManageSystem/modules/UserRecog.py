from sqlalchemy import Table, MetaData
import numpy as np

from app import db


class UserRecog(db.Model):
    __table__ = Table('t_faceconfig', MetaData(bind=db.engine), autoload=True)

    def insert(self, name, is_adm, data: np.ndarray):  # 插入新的人脸的编码值
        if type(data) is np.ndarray:
            row = UserRecog(name=name, is_adm=is_adm, encode=data.tobytes())
            db.session.add(row)
            db.session.commit()
        db.session.close()

    def find_by_name(self, name):  # 根据名称查找用户是否注册人脸
        row = db.session.query(UserRecog.encode).filter(UserRecog.name == name).first()
        db.session.close()
        return row

    def getencode(self, name, is_adm):  # 根据名字获取人脸编码
        row = db.session.query(UserRecog.encode).filter(UserRecog.name == name, UserRecog.is_adm == is_adm).first()
        if row:
            data = np.frombuffer(row.encode, dtype=np.float)
        db.session.close()
        return data  # 返回np类型的编码

    def getall(self):  # 获取所有人脸编码
        row = db.session.query(UserRecog.name, UserRecog.is_adm, UserRecog.encode).all()
        db.session.close()
        return row
