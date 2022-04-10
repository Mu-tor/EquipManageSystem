from flask import Blueprint, render_template, session, request

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


@equipment.route("/broEquip")
def bro_equip():
    equip = Equipment()
    equips = equip.show_eqp_all()
    name = request.args.get("name")
    pwd = request.args.get("pwd")
    results = []
    i = 0
    for equip in equips:
        result = {"equip": equip, "index": i}
        i += 1
        results.append(result)
    return render_template("booking.html", results=results, is_addr=0, username=session.get('user'))
