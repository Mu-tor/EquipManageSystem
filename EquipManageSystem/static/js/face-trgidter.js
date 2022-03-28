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

// 验证用户进行注册
function register(timer, error) {
    context.drawImage(video, 0, 0, 640, 480);
    //获得截图base64编码
    let imgData = canvas.toDataURL("image/png", 0.8);
    //ajax发送校验
    $.ajax({
        url: "/register_face",
        type: "POST",
        dataType: 'json',
        data: {"imgData": imgData},
        success: function (data) {
            if (data.result == "fail") {
                $("#result_tag").text("检测不出人脸");
            } else {
                endRecognize(timer, error);
                if (data.result == "repetition") {
                    alert("请勿重复注册！！");
                    $('#registerModal').modal('show');
                } else {
                    alert("人脸注册成功！");
                    location.reload(true);
                }
                $('#faceModal').modal('hide');
            }
        }
    })
}

document.getElementById("register_face").addEventListener("click", function () {
    let timer;
    let error;
    $('#faceModal').modal('show');
    open_video();
    timer = setInterval(function () { // 2秒检测一次
        register(timer, error);
    }, 2000);
    error = setInterval(function () { // 检测不到人脸进行提醒
        alert('检测不到人脸，请重试！！')
        $('#faceModal').modal('hide');
    }, 4900);
    setTimeout(function () {
        endRecognize(timer, error)
    }, 5000);
});
