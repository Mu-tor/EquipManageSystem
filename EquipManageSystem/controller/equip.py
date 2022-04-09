from flask import Blueprint, render_template, session

from modules.equipment import Equipment

equipment = Blueprint("equipment", __name__)


@equipment.route("/equipmentShow")
def equip_show():
    equip = Equipment()
    row = equip.show_eqp_all()
    return render_template("booking.html", equips=row, is_addr=0, username=session.get('user'))
