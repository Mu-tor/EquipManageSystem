function getUserMedia(constraints, success, error) {
    if (navigator.mediaDevices.getUserMedia) {
        //最新的标准API
        navigator.mediaDevices.getUserMedia(constraints).then(success).catch(error);
    } else if (navigator.webkitGetUserMedia) {
        //webkit核心浏览器
        navigator.webkitGetUserMedia(constraints, success, error)
    } else if (navigator.mozGetUserMedia) {
        //firfox浏览器
        navigator.mozGetUserMedia(constraints, success, error);
    } else if (navigator.getUserMedia) {
        //旧版API
        navigator.getUserMedia(constraints, success, error);
    }
}

let video = document.getElementById('video');

video.controls = false;
let canvas = document.getElementById('canvas');
//返回一个用于在画布上绘图的环境
let context = canvas.getContext('2d');

context.arc(250, 250, 200, 0, 0.75 * Math.PI, false);

function success(stream) {
    //兼容webkit核心浏览器
    let CompatibleURL = window.URL || window.webkitURL;
    //将视频流设置为video元素的源
    //video.src = CompatibleURL.createObjectURL(stream);
    video.srcObject = stream;
    video.play();
}

function error(error) {
    console.log(`访问用户媒体设备失败${error.name}, ${error.message}`);
    alert("访问用户媒体设备失败")
}

function open_video() { // 打开摄像头并显示
    if (navigator.mediaDevices.getUserMedia || navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia) {
        //调用用户媒体设备, 访问摄像头
        getUserMedia({video: {width: 640, height: 480}}, success, error);
    } else {
        alert('不支持访问用户媒体');
    }
}


function closeVideo() { // 关闭摄像头
    video.srcObject.getTracks()[0].stop();
    video.srcObject.getTracks()[0].stop();
}

function endRecognize(timer, error) {
    clearInterval(timer); // 停止检测
    clearInterval(error); // 取消提示
    closeVideo();
}

function face_recognize(timer, error) { // 人脸验证登录
    let imgData
    let url
    context.drawImage(video, 0, 0, 500, 380);
    //获得截图base64编码
    imgData = canvas.toDataURL("image/png", 0.8);
    //ajax发送校验
    $.ajax({
        url: "/login_face",
        type: "POST",
        dataType: 'json',
        data: {"imgData": imgData},
        success: function (data) {
            if (data.result == "fail") {
                $("#result_tag").text("检测不出人脸");
            } else if (data.result == "unknown") {
                $("#result_tag").text("未知人员");
                alert("请先注册！！！")
                endRecognize(timer, error);  // 停止检测
                $("#faceModal").modal('hide');
            } else {
                endRecognize(timer, error);
                alert(data.name + "登陆成功！！！");
                endRecognize(timer, error); //停止检测
                if (data.is_adm == 0) {
                    url = '/user/'
                } else {
                    url = '/admin/'
                }
                url += data.name
                location.replace(url);
            }
        }
    })
}

// 验证用户人脸进行登录
document.getElementById("check").addEventListener('click', function () {
    let timer;
    let error;
    open_video();
    timer = setInterval(function () { // 每秒检测一次
        face_recognize(timer, error);
    }, 1000);
    error = setInterval(function () { // 检测不到人脸进行提醒
        alert('检测不到人脸，请重试！！');
        $('#faceModal').modal('hide');
    }, 4800);
    setTimeout(function () {
        endRecognize(timer, error);// 五秒后还未检测到人脸则停止检测
    }, 5000);
})


document.getElementById("register").addEventListener("click", function () {
    if (!checkpwd())
        return
    let uname = document.getElementById("uname").value
    let password = document.getElementById("password").value
    let sex = $('input[name=sex]:checked').val();
    let birthday = document.getElementById("birthday").value;
    let tel = document.getElementById("tel").value;
    //ajax发送校验
    $.ajax({
        url: "/register_face",
        type: "POST",
        dataType: 'json',
        data: {"imgData": imgData, "uname": uname, "password": password, "sex": sex, "birthday": birthday, "tel": tel},
        success: function (data) {
            if (data.result == "fail") {
                $("#result_tag").text("检测不出人脸");
            } else {
                endRecognize(timer, error);
                if (data.result == "repetition") {
                    alert("请勿重复注册！！");
                    $('#registerModal').modal('show');
                } else {
                    alert(uname + "注册成功！");
                }
                $('#faceModal').modal('hide');
            }
        }
    })
})

function checkpwd() {

    let name = $("input#name1");
    let pwd1 = $("input#password");
    let pwd2 = $("input#passwd2");
    let tel = $("input#tel");
    let checkbox = $("input#checkbox").prop("checked");
    if (name.val() == "" || pwd1.val() == "") {
        alert("账号或密码不能为空！！")
        return false;
    }

    if (pwd1.val() != pwd2.val()) {
        alert("两次输入密码不一致！")
        pwd1.innerHTML = "";
        pwd2.innerHTML = "";
        return false;
    }

    if (!checkbox) {
        alert("请选中条款");
        return false;
    }

    if (!ValidatePhone(tel.val())) {
        alert("请输入正确的电话号码！！！");
        return false;
    }

    return true;
}

function ValidatePhone(val) {
    let isPhone = /^([0-9]{3,4}-)?[0-9]{7,8}$/;//手机号码
    let isMob = /^0?1[3|4|5|8][0-9]\d{8}$/;// 座机格式
    if (isMob.test(val) || isPhone.test(val)) {
        return true;
    } else {
        return false;
    }
}
