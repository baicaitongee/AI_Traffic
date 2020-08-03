#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, jsonify
import sqlite_test
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    # from camera import Camera
    from camera_opencv import Camera

import base64
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    rootdir = r"./static/pic_history"
    filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
    filelist = filelist[-7:]  # 显示最后n张图片，n为里面的数值
    # for f in filelist:
    #     filepath = os.path.join(rootdir, f)  # 将文件名映射成绝对路劲
    print(filelist)
    return render_template('index.html', filelist=filelist)

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/shuaxin',methods=['POST','GET'])  # 柏财通 在这接数据库 柏财通 在这接数据库 柏财通 在这接数据库 柏财通 在这接数据库 柏财通 在这接数据库 柏财通 在这接数据库
def shuaxin():  # shuaxin函数实现获取数据库数据和实现刷新
    context = {"data1": 1,   # 赋值给context
               "data2": 2}
    context=list(sqlite_test.query_trash())

    # 大类
    context1 = [1, 2, 3, 5,1,1,1]  # 小类
    return jsonify(context,context1)  # 返回数值到页面 ，里面有几个数便嵌套几个[],现在返回页面就变成[[1, 2, 3, 4],[5, 2, 3, 5]]

@app.route('/shuaxintu',methods=['POST','GET'])
def shuaxintu():  # shuaxintu函数实现图片刷新
    rootdir = r".\static\pic_history"
    filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
    filelist = filelist[-7:]  # 显示最后n张图片，n为里面的数值
    return jsonify(filelist)  # 返回数值到页面 ，里面有几个数便嵌套几个[],现在返回页面就变成[[1, 2, 3, 4],[5, 2, 3, 5]]


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        #frame=get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_frame():
    #解析图片数据
    img = base64.b64decode(str(request.form['image2']))
    image_data = np.fromstring(img, np.uint8)
    image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    #cv2.imwrite('get_image/01.jpg', image_data)
    #print(image_data)
    return image_data
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.137.70', port=5001,threaded=True)
