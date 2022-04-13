import os
import random
from datetime import datetime


from flask import Blueprint, render_template, session, make_response, send_from_directory, url_for, redirect, request

from app import app
from common.utility import get_table
from modules.address import Address
from modules.admins import Admins
from modules.booking import Booking
from modules.brodtl import Brodtl
from modules.equipment import Equipment
from modules.record import Record
from modules.users import Users
from modules.notice import Notice

admin = Blueprint("admin", __name__)


@admin.route('/<string:name>', methods=['get', 'post'])  # 人脸登录
def admin_home(name):
    admins = Admins()
    row = admins.find_admin_by_admnane(name)
    is_face = True
    session["admin"] = row.admname
    messnum = admin_message_num()
    return render_template("manager.html", person=row, messageNum=messnum, is_face=is_face, info="登陆成功!!")


def wait_process():  # 待处理事务
    book = Booking()
    row = book.find_all_by_isagree(-1)
    return row


def admin_message_num():  # 待处理事务数
    return len(wait_process())


def get_details(works):  # 获得记录详情
    brotli = Brodtl()
    addr = Address()
    users = Users()
    equip = Equipment()
    results = []
    for work in works:
        details = brotli.find_book_by_bid(work.bid)  # 详情
        user = users.find_user_by_id(work.uid)
        result = {"booking": work, "details": details, "user": user}
        if details.is_addr == 1:
            row = addr.find_addr_by_id(details.addrid)
            result.setdefault("address", row)
        else:
            row = equip.find_eqp_by_id(details.eqpid)
            result.setdefault("equipment", row)
        results.append(result)
    return results


@admin.route('/download', methods=['GET', 'POST'])  # 下载记录表格
def download_table():
    book = Booking()
    record = Record()
    admins = Admins()
    bookings = book.find_all()  # 获取所有记录
    results = get_details(bookings)
    datalist = []
    for result in results:
        data = [result['booking'].bid]  # 序号
        if result['details'].is_addr == 1:  # 类型、名称
            data.append("场地")
            data.append(f"{result['address'].addr_name}({result['address'].address})")
        else:
            data.append("器材")
            data.append(result['equipment'].eqp_name)
        data.append(result['details'].bro_num)  # 数量
        data.append(result['booking'].bro_time.strftime('%Y-%m-%d'))  # 预约日期
        if result['booking'].is_agree != -1:  # 填加处理人信息和记录表信息
            recd = record.find_rec_by_bid(result['booking'].bid)
            if recd.is_return == 0:
                retdate = "未归还"
            else:
                retdate = recd.rtn_date.strftime('%Y-%m-%d')  # 已归还，显示日期
            adm = admins.find_admin_by_id(recd.admid)
            adminname = adm.admname
            if result['booking'].is_agree == 0:
                retdate = "已驳回"
        else:
            retdate = "未审核"
            adminname = "无"
        data.append(retdate)  # 归还日期
        username = result['user'].username
        if result['user'].is_out == 1:  # 外部人员
            username += "外部人员"
        data.append(username)  # 预约人
        data.append(adminname)  # 处理人
        datalist.append(data)
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_rand = random.randint(1, 99)
    get_table(datalist, date, file_rand)
    response = make_response(
        send_from_directory(os.path.join(app.static_folder, "document"),
                            f"器材借用记录报表{date}-{file_rand}.xls".encode('utf-8').decode('utf-8'), as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(
        "器材借用记录报表.xls".encode().decode('latin-1'))
    return response


@admin.route('/approval', methods=['GET', 'POST'])  # 审核
def admin_approval():
    bookings = wait_process()  # 获取待处理事务
    results = get_details(bookings)
    return render_template("ProcessApprovals.html", results=results, admin=session.get('admin'))


@admin.route('/decision/<int:bid>/<string:deci>', methods=['GET', 'POST'])
def admin_decision(bid, deci):
    admins = Admins()
    record = Record()
    admin_name = session.get('admin')
    adm = admins.find_admin_by_admnane(admin_name)
    if deci == 'disagree':
        record.insert_rec(bid, adm.admid, "驳回", 0, -1)
    else:
        record.insert_rec(bid, adm.admid, "同意", 1)
    return redirect(url_for('admin.admin_approval'))


@admin.route('/look_record', methods=['GET', 'POST'])  # 查看所有记录
def admin_look_record():
    book = Booking()
    record = Record()
    admins = Admins()
    bookings = book.find_all()  # 获取所有记录
    results = get_details(bookings)
    for result in results:
        if result['booking'].is_agree != -1:  # 填加处理人信息和记录表信息
            recd = record.find_rec_by_bid(result['booking'].bid)
            result.setdefault("record", recd)
            adm = admins.find_admin_by_id(recd.admid)
            result.setdefault("admin", adm)
    return render_template("ManagerLookRecord.html", results=results, admin=session.get('admin'))


@admin.route('/look_eqp', methods=['GET', 'POST'])  # 查看所有记录
def admin_look_eqp():
    results = Equipment().show_eqp_all()
    return render_template("Registerquipment.html", results=results, admin=session.get('admin'))


@admin.route('/delete_eqp/<int:id>', methods=['GET', 'POST'])  # 删除
def admin_delete_eqp(id):
    Equipment().delete(id)
    return redirect(url_for("admin.admin_look_eqp"))


@admin.route('/change', methods=['get', 'POST'])  # 修改
def admin_search_eqp():
    id = request.form.get('id')
    result = Equipment().find_eqp_by_id(id)
    name = request.form.get("name")
    num = request.form.get("num")
    result.update_eqp(name, num)
    return redirect(url_for("admin.admin_look_eqp"))

@admin.route('/insert', methods=['get', 'POST'])  # 添加
def admin_insert_eqp():
    name = request.form.get("name")
    num = request.form.get("num")
    Equipment().insert_eqp(name, num)
    return redirect(url_for("admin.admin_look_eqp"))

@admin.route('/look_notice', methods=['GET', 'POST'])  # 查看所有公告记录
def admin_look_notice():
    results = Notice().find_all()
    return render_template("ToBulletinboard.html", results=results, admin=session.get('admin'))

@admin.route('/add_notice', methods=['GET', 'POST'])  # 发布公告
def admin_add_notice():
    content = request.form.get("content")
    id=Admins().find_admin_by_admnane(session.get('admin')).admid
    Notice().insert_notice(id ,content )
    return redirect(url_for("admin.admin_look_notice"))



@admin.before_request
def before():
    if session.get('islogin') != 'true':
        return render_template('login.html', info="请先登录或注册！！")
    else:
        pass
