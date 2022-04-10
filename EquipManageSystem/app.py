import base64
import hashlib
import os
import random
import face_recognition

from io import BytesIO

from flask import Flask, render_template, session, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/laboratory?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 设置session密钥
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
from common import utility, face_recognize


@app.route("/")
def login():
    #   table测试
    # datalist = [['9月12日', '尺子', '100', '李四', '未还', '完好'],
    #             ['9月14日', '篮球', '37', '王五', '未还', '破损']]
    # utility.get_table(datalist)

    return render_template("index.html")


@app.route("/model")
def model():
    return render_template("model.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error404.html'), 404


@app.route("/verify")  # 登录
def verify():
    return render_template("login.html")


@app.route("/login", methods=['post', 'get'])  # 登录
def person_login():
    from modules.admins import Admins
    from modules.users import Users
    from modules.UserRecog import UserRecog
    users = Users()
    admins = Admins()
    name = request.form["uname"]
    pwd = request.form["pwd"]
    is_adm = 0
    row = users.find_user_by_uname(name)

    session['islogin'] = 'true'  # 删除
    session["user"] = row.username  # 删除
    return render_template("UserHome.html", person=row, is_face=True, info="登陆成功!!")  # 删除
    #
    # if row is None:  # 查询是否为管理员登录
    #     is_adm = 1
    #     row = admins.find_admin_by_admnane(name)
    # m = hashlib.md5()
    # m.update(pwd.encode("utf8"))
    # print(m.hexdigest())
    # vcode = request.form.get("vcode").strip().lower()
    # if len(vcode) == 0:
    #     return render_template("login.html", info="验证码为空")
    # if row is not None:
    #     svcode = session.get("vcode")
    #     if svcode == vcode:
    #         if m.hexdigest() == row.password:
    #             is_face = False
    #             if UserRecog().find_by_name(name) is not None:
    #                 is_face = True
    #             session['islogin'] = 'true'
    #             if is_adm == 0:  # 用户登录
    #                 session["user"] = row.username
    #                 return render_template("UserHome.html", person=row, is_face=is_face, info="登陆成功!!")
    #             else:  # 管理员登录
    #                 session["admin"] = row.admname
    #                 return render_template("manager.html", person=row, is_face=is_face, info="登陆成功!!")
    #         else:
    #             return render_template("login.html", info="密码错误!!")
    #     else:
    #         return render_template("login.html", info="验证码不正确")  # 根据返回显示验证码不正确
    # else:
    #     return render_template("login.html", info="用户不存在!!")


@app.route('/login_face', methods=['post'])  # 人脸登录
def recognize():
    is_adm = -1
    name = "unknown"
    if request.method == "POST":
        img_base64 = request.form["imgData"]
        file_rand = random.randint(1, 9999)
        img_data = base64.b64decode(img_base64.split(",")[1])
        file_paths = os.path.join(app.static_folder, "temp_face", "{}.png".format(file_rand))
        with open(file_paths, "wb+") as f:
            f.write(img_data)
        result = face_recognize.check_face(file_paths)
        if result == "fail":  # 未识别到人脸
            os.remove(file_paths)
        else:
            person = face_recognize.compareencode(file_paths)
            if person is not None:
                is_adm = person[1]
                name = person[0]
                session['islogin'] = 'true'
            else:  # 未知人员
                result = "unknown"
        return jsonify({"result": result, "is_adm": is_adm, "name": name})


@app.route('/register_face', methods=['post'])  # 进行人脸注册
def register_face():
    from modules.UserRecog import UserRecog
    if request.method == "POST":
        img_base64 = request.form["imgData"]
        img_data = base64.b64decode(img_base64.split(",")[1])
        file_rand = random.randint(1, 9999)
        temp_paths = os.path.join(app.static_folder, "temp_face", "{}.png".format(file_rand))
        with open(temp_paths, "wb+") as f:
            f.write(img_data)
        result = face_recognize.check_face(temp_paths)
        if result == "fail":
            os.remove(temp_paths)  # 识别不到人脸
        elif face_recognize.compareencode(temp_paths):
            os.remove(temp_paths)
            result = "repetition"  # 重复注册
        else:
            frame = face_recognition.load_image_file(temp_paths)
            face_encoding = face_recognition.face_encodings(frame)[0]
            if session.get('user') is not None:
                name = session.get('user')
                is_adm = 0
            else:
                name = session.get('admin')
                is_adm = 1
            UserRecog().insert(name, is_adm, face_encoding)  # 保存编码到数据库中
        return jsonify({"result": result})


# #  拦截器
# @app.before_request
# def before():
#     url = request.path
#     # 在列表中设置白名单
#     pass_list = ['/', '/reg', '/login', '/vcode', '/verify']
#     # 静态资源如图片，css和js代码等通过后缀名来放行
#     suffix = url.endswith(".png") or url.endswith(".jpg") or url.endswith(".css") or url.endswith(
#         ".js") or url.endswith(".ico") or url.endswith("*")
#     if url in pass_list or suffix:
#         pass
#     elif session.get('islogin') != 'true':
#         return render_template('login.html', info="请先登录或注册！！")


@app.route('/vcode')  # 验证码
def get_code():
    im, code = utility.get_verify_code()
    buf = BytesIO()
    im.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error404.html'), 404


if __name__ == '__main__':
    from controller.user import user
    from controller.admin import admin
    from controller.addr import address
    from controller.equip import equipment

    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(address)
    app.register_blueprint(equipment)

    app.run()
