from datetime import datetime

from flask import Blueprint, render_template, session, url_for, redirect, request, jsonify

from modules.address import Address
from modules.booking import Booking
from modules.brodtl import Brodtl

address = Blueprint("address", __name__)


@address.route("/addressShow")
def address_show():
    addre = Address()
    addrs = addre.show_addr_all()
    results = []
    i = 0
    for addr in addrs:
        result = {"addr": addr, "index": i}
        i += 1
        results.append(result)
    return render_template("booking.html", results=results, is_addr=1, username=session.get('user'))


@address.route("/broAddress", methods=['get', 'post'])  # 预约场地
def bro_equip():
    booking = Booking()
    brodtl = Brodtl()
    # 获取前端传入数据
    addrid = request.form.get("addrid")
    broDate = request.form.get("broDate")
    uid = session.get('uid')
    if booking.find_book_by_date_addr(datetime.strptime(broDate, '%Y-%m-%d'), addrid) is None:
        # 可借
        book = booking.insert_book(uid, broDate)  # 插入booking表
        brodtl.insert_bro(book.bid, None, addrid, 1)  # 插入详情表
        result = "success"
    else:
        result = "fail"  # 不可借
    return jsonify({"result": result})
