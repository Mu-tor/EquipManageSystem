from flask import Blueprint, render_template, session, request

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
    return render_template("UserHome.html", person=row, is_face=is_face, info="登陆成功!!")


@user.route('/myrecord', methods=['get', 'post'])
def user_record():
    username = session.get('user')
    book = Booking()
    addr = Address()
    equip = Equipment()
    record = Record()
    borrow = None
    records = book.find_all_by_username(username)
    if records[0].Booking.is_agree == 1:
        borrow = record.find_rec_by_bid(records[0].Booking.bid)  # 借用记录表，同意借阅
    if records[0].Brodtl.is_addr == 1:
        row = addr.find_addr_by_id(records[0].Brodtl.addrid)
    else:
        row = equip.find_eqp_by_id(records[0].Brodtl.eqpid)
    return render_template("myrecord.html", records=records, equipment=row, username=username, borrow=borrow)


@user.before_request
def before():
    if session.get('islogin') != 'true':
        return render_template('login.html', info="请先登录或注册！！")
    else:
        pass
