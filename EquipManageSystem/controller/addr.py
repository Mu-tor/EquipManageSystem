from flask import Blueprint, render_template, session

from modules.address import Address

address = Blueprint("address", __name__)


@address.route("/addressShow")
def address_show():
    addr = Address()
    row = addr.show_addr_all()
    return render_template("booking.html", addrs=row, is_addr=1, username=session.get('user'))
