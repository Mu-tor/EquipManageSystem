import face_recognition

# 获取脸库的所有人脸特征
import numpy as np

# 检测照片是否存在人脸
from modules.UserRecog import UserRecog


def check_face(filename):  # 查询是否含有人脸
    frame = face_recognition.load_image_file(filename)
    face_location = face_recognition.face_locations(frame)
    if len(face_location) == 0:
        return "fail"
    else:
        return "success"


def compareencode(img_file):  # 按图片识别人脸，返回姓名,不存在返回None
    userRecog = UserRecog()
    frame = face_recognition.load_image_file(img_file)
    encode = face_recognition.face_encodings(frame)[0]
    rows = userRecog.getall()
    for row in rows:
        data = np.frombuffer(row.encode, dtype=np.float)
        match = face_recognition.compare_faces([data], encode, tolerance=0.5)
        if match[0]:
            return [row.name, row.is_adm]
    return None
