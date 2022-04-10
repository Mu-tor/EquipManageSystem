from flask import Blueprint, render_template, session

from modules.address import Address
from modules.booking import Booking
from modules.equipment import Equipment
from modules.record import Record
from modules.users import Users

user = Blueprint("user", __name__)


@user.route('/<string:name>', methods=['get', 'post'])  # 人脸登录
def user_home(name):
    users = Users()
    row = users.find_user_by_uname(name)
    is_face = True  # 用户已注册人脸
    session["user"] = row.username
    messnum = user_message_num(row.uid)
    return render_template("UserHome.html", person=row, messageNum=messnum, is_face=is_face, info="登陆成功!!")


def user_message_num(uid):  # 根据用户id获取待归还数
    record = Record()
    messnum = len(record.find_all_by_isrtn(0, uid))
    return messnum


def get_result():
    booking = Booking()
    addr = Address()
    equip = Equipment()
    record = Record()
    results = []
    books = booking.find_all_by_username(session.get('user'))
    for book in books:
        result = {"record": book}
        if book.Booking.is_agree == 1:
            borrow = record.find_rec_by_bid(book.Booking.bid)  # 借用记录表，同意借阅
            result.setdefault("borrow", borrow)
        if book.Brodtl.is_addr == 1:
            row = addr.find_addr_by_id(book.Brodtl.addrid)
            result.setdefault("address", row)
        else:
            row = equip.find_eqp_by_id(book.Brodtl.eqpid)
            result.setdefault("equipment", row)
        results.append(result)
    return results


@user.route('/myrecord', methods=['get', 'post'])
def user_record():
    results = get_result()
    return render_template("myrecord.html", results=results, username=session.get('user'))


@user.route('/lookrecord', methods=['get', 'post'])
def user_lookrecord():
    results = get_result()
    return render_template("lookrecord.html", results=results, username=session.get('user'))


@user.before_request
def before():
    if session.get('islogin') != 'true':
        return render_template('login.html', info="请先登录或注册！！")
    else:
        pass
