from flask import Blueprint, render_template, session

from modules.address import Address

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
