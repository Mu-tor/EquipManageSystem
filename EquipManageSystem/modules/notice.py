from sqlalchemy import MetaData, Table

from app import db


class Notice(db.Model):  # 公告表
    __table__ = Table('t_notice', MetaData(bind=db.engine), autoload=True)

    def find_notice_by_notid(self, notid):
        row = db.session.query(Notice).filter(Notice.notid == notid).first()
        return row

    # 按管理员找他发布的公告
    def find_all_by_admid(self, admid):
        row = db.session.query(Notice).filter(Notice.admid == admid).all()
        return row

    # 按内容找
    def find_notice_by_content(self, ctn):
        row = db.session.query(Notice).filter(Notice.content == ctn).first()
        return row

    # 查询所有公告
    def find_all(self):
        row = db.session.query(Notice).all();
        return row

    # 添加
    def insert_notice(self, admid, ctn):
        n = Notice(admid=admid, content=ctn)
        db.session.add(n)
        db.session.commit()

    # 修改
    def update_notice(self, notc):
        self.notid = notc.notid
        self.admid = notc.admid
        self.content = notc.content
        db.session.commit()

    # 删除
    def delete(self, id):
        row = Notice().find_notice_by_notid(id)
        db.session.delete(row)
        db.session.commit()
