from flask import Blueprint, render_template, session

from modules.address import Address
from modules.admins import Admins
from modules.booking import Booking
from modules.brodtl import Brodtl
from modules.equipment import Equipment
from modules.users import Users

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


@admin.route('lookrecord', methods=['GET', 'POST'])  # 查看申请
def admin_lookrecord():
    brotli = Brodtl()
    addr = Address()
    users = Users()
    equip = Equipment()
    results = []
    bookings = wait_process()
    for booking in bookings:
        details = brotli.find_book_by_bid(booking.bid)  # 详情
        user = users.find_user_by_id(booking.uid)
        result = {"booking": booking, "details": details, "user": user}
        if details.is_addr == 1:
            row = addr.find_addr_by_id(details.addrid)
            result.setdefault("address", row)
        else:
            row = equip.find_eqp_by_id(details.eqpid)
            result.setdefault("equipment", row)
        results.append(result)
    return render_template("ManagerLookRecord.html", results=results, admin=session.get('admin'))


@admin.before_request
def before():
    if session.get('islogin') != 'true':
        return render_template('login.html', info="请先登录或注册！！")
    else:
        pass
