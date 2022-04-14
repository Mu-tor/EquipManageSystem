from datetime import datetime

from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify

from modules.booking import Booking
from modules.brodtl import Brodtl
from modules.equipment import Equipment

equipment = Blueprint("equipment", __name__)


@equipment.route("/equipmentShow")
def equip_show():
    equip = Equipment()
    equips = equip.show_eqp_all()
    results = []
    i = 0
    for equip in equips:
        result = {"equip": equip, "index": i}
        i += 1
        results.append(result)
    return render_template("booking.html", results=results, is_addr=0, username=session.get('user'))


@equipment.route("/broEquip", methods=['get', 'post'])
def bro_equip():
    equip = Equipment()
    booking = Booking()
    brodtl = Brodtl()
    # 获取前端传入数据
    eqpid = request.form.get("eqpid")
    bro_num = int(request.form.get("broNum"))
    print(bro_num)
    uid = session.get('uid')
    row = equip.find_eqp_by_id(eqpid)
    if row.num >= bro_num:
        book = booking.insert_book(uid, datetime.now().strftime("%Y-%m-%d"))  # 插入booking表
        brodtl.insert_bro(book.bid, eqpid, None, 0, bro_num)  # 插入详情表
        result = "success"
    else:
        result = "fail"  # 不可借
    return jsonify({"result": result})
