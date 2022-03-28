from flask import Blueprint, render_template, session, request
from modules.users import Users

user = Blueprint("user", __name__)


@user.route('/<string:name>', methods=['get', 'post'])  # 人脸登录
def user_home(name):
    users = Users()
    row = users.find_user_by_uname(name)
    is_face = True  # 用户已注册人脸
    session["user"] = row.username
    return render_template("UserHome.html", person=row, is_face=is_face, info="登陆成功!!")


@user.before_request
def before():
    if session.get('islogin') != 'true':
        return render_template('login.html', info="请先登录或注册！！")
    else:
        pass
