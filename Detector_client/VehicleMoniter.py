import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
from vehicle import vehicle
import PIL.Image as Image
from collections import defaultdict
from io import StringIO
from PIL import Image
import time
from multiprocessing.pool import ThreadPool
import threading
import time
import numpy as np
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import json
import re

from hyperlpr import *

import requests
import base64

#1111==========================================超参数定义======================================

if tf.__version__ < '1.4.0':
	raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')
# This is needed to display the images.


# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")


from utils import label_map_util

from utils import visualization_utils as vis_util

# What model to download.
#MODEL_NAME = './Cars'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
#PATH_TO_CKPT = "Cars/output_inference_graph.pb"

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('Cars', 'car_label_map.pbtxt')

NUM_CLASSES = 1



#api = openalpr_api.DefaultApi()
#secret_key = 'sk_9bbee5c20ac912ecef2b825e'
country = 'us'
recognize_vehicle = 0
state = ''
return_image = 0
topn = 1
prewarp = ''
vehicles=[]
line=[]
pos=[]
# 单击屏幕的次数
#clickpoint=0

#11111==========================================超参数定义======================================
#22222==========================================功能函数定义======================================
def plate_recognition(named):
	try:
		img=cv2.imread(named)
		plate=HyperLPR_plate_recognition(img)
		if len(plate) == 0:
			print("没检测到！！！")
			pass
		#print(plate)
		print(len(plate))
		X1=plate[0][2][0]
		Y1=plate[0][2][1]
		X2=plate[0][2][2]
		Y2=plate[0][2][3]
		print('test:{}'.format(plate[0][0]),'车牌号坐标：{}，{}，{}，{}'.format(X1,Y1,X2,Y2))
		rimg=img[Y1:Y2,X1:X2]
		frame3=rimg
		img3 = Image.fromarray(frame3)
		w,h=img3.size
		asprto=w/h
		frame3=cv2.resize(frame3,(150,int(150/asprto)))
		cv2image3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGBA)
		img3 = Image.fromarray(cv2image3)
		imgtk3 = ImageTk.PhotoImage(image=img3)
		display4.imgtk = imgtk3 #Shows frame for display 1
		display4.configure(image=imgtk3)
		display5.configure(text=plate[0][0])
	except Exception as e:
		print('Exception:\n',e)
	
def matchVehicles(currentFrameVehicles,im_width,im_height,image):
	if len(vehicles)==0:
		for box,color in currentFrameVehicles:
			(y1,x1,y2,x2)=box
			(x,y,w,h)=(x1*im_width,y1*im_height,x2*im_width-x1*im_width,y2*im_height-y1*im_height)
			X=int((x+x+w)/2)
			Y=int((y+y+h)/2)
			if Y>yl5:
				#cv2.circle(image,(X,Y),2,(0,255,0),4)
				#print('Y=',Y,'  y1=',yl1)
				vehicles.append(vehicle((x,y,w,h)))


	else:
		for i in range(len(vehicles)):
			vehicles[i].setCurrentFrameMatch(False)
			vehicles[i].predictNext()
		for box,color in currentFrameVehicles:
			(y1,x1,y2,x2)=box
			(x,y,w,h)=(x1*im_width,y1*im_height,x2*im_width-x1*im_width,y2*im_height-y1*im_height)
			#print((x1*im_width,y1*im_height,x2*im_width,y2*im_height),'\n',(x,y,w,h))
			index = 0
			ldistance = 999999999999999999999999.9
			X=int((x+x+w)/2)
			Y=int((y+y+h)/2)
			if Y>yl5:
				#print('Y=',Y,'  y1=',yl1)
				#cv2.circle(image,(X,Y),4,(0,0,255),8)
				for i in range(len(vehicles)):
					if vehicles[i].getTracking() == True:
						#print(vehicles[i].getNext(),i)
						distance = ((X-vehicles[i].getNext()[0])**2+(Y-vehicles[i].getNext()[1])**2)**0.5

						if distance<ldistance:
							ldistance = distance
							index = i


				diagonal=vehicles[index].diagonal

				if ldistance < diagonal:
					vehicles[index].updatePosition((x,y,w,h))
					vehicles[index].setCurrentFrameMatch(True)
				else:
					#blue for last position
					#cv2.circle(image,tuple(vehicles[index].points[-1]),2,(255,0,0),4)
					#red for predicted point
					#cv2.circle(image,tuple(vehicles[index].getNext()),2,(0,0,255),2)
					#green for test point
					#cv2.circle(image,(X,Y),2,(0,255,0),4)

					#cv2.imshow('culprit',image)
					#time.sleep(5)
					#print(diagonal,'               ',ldistance)
					vehicles.append(vehicle((x,y,w,h)))

		for i in range(len(vehicles)):
			if vehicles[i].getCurrentFrameMatch() == False:
				vehicles[i].increaseFrameNotFound()

    #print(len(vehicles))

def checkRedLightCrossed(img):
	global count
	for v in vehicles:
		if v.crossed==False and len(v.points)>=2:
			x1,y1=v.points[0]
			x2,y2=v.points[-1]
			if y1>yl3 and y2<yl3:
				count+=1
				v.crossed=True
				bimg=img[int(v.rect[1]):int(v.rect[1]+v.rect[3]), int(v.rect[0]):int(v.rect[0]+v.rect[2])]
				frame2=bimg
				img2 = Image.fromarray(frame2)
				w,h=img2.size
				asprto=w/h
				frame2=cv2.resize(frame2,(250,int(250/asprto)))
				cv2image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
				img2 = Image.fromarray(cv2image2)
				imgtk2 = ImageTk.PhotoImage(image=img2)
				display2.imgtk = imgtk2 #Shows frame for display 1
				display2.configure(image=imgtk2)
				#cv2.imshow('BROKE',bimg)
				named='Rule Breakers/culprit'+str(time.time())+'.jpg'
				
				cv2.imwrite(named,bimg)
				



				tstop = threading.Event()
				thread = threading.Thread(target=plate_recognition, args=(named,))
				thread.daemon = True
				thread.start()
				

				#cv2.imwrite('culprit.png',bimg)
	#display3.configure(text=count)

def checkSpeed(ftime,img):
	for v in vehicles:
		if v.speedChecked==False and len(v.points)>=2:
			x1,y1=v.points[0]
			x2,y2=v.points[-1]
			if y2<yl1 and y2>yl3 and v.entered==False:
				v.enterTime=ftime
				v.entered=True
			elif  y2<yl3  and y2 > yl5 and v.exited==False:
				v.exitTime=ftime
				v.exited==False
				v.speedChecked=True
				speed=60/(v.exitTime-v.enterTime)
				print(speed)
				bimg=img[int(v.rect[1]):int(v.rect[1]+v.rect[3]), int(v.rect[0]):int(v.rect[0]+v.rect[2])]
				frame2=bimg
				img2 = Image.fromarray(frame2)
				w,h=img2.size
				asprto=w/h
				frame2=cv2.resize(frame2,(250,int(250/asprto)))
				cv2image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
				img2 = Image.fromarray(cv2image2)
				imgtk2 = ImageTk.PhotoImage(image=img2)
				display2.imgtk = imgtk2 #Shows frame for display 1
				display2.configure(image=imgtk2)
				display3.configure(text=str(speed)[:5]+'Km/hr')
				if speed>60:
					
					#cv2.imshow('BROKE',bimg)
					named='Rule Breakers/culprit'+str(time.time())+'.jpg'
					cv2.imwrite(named,bimg)
				
					tstop = threading.Event()
					thread = threading.Thread(target=plate_recognition, args=(named,))
					thread.daemon = True
					thread.start()

def stream():
    global masterframe
    global started
    global c
    global tim
    cap=cv2.VideoCapture('vid1.mp4')
    while True:
        started,masterframe=cap.read()
        time.sleep(0.034)

# def regionofinterest(window):
# 	def imgclick(event):
# 		if clickpoint < 6:
# 			x = int(canvas.canvasx(event.x))
# 			y = int(canvas.canvasy(event.y))
# 			line.append((x, y))
# 			pos.append(canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair"))
# 			pos.append(canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair"))
# 			clickpoint += 1
# 		if self.counter == 6:
#             #unbinding action with mouse-click
# 			self.canvas.unbind("<Button-1>")
# 			window.config(cursor="arrow")
# 			clickpoint = 0

# 			xl1=line[0][0]
# 			yl1=line[0][1]
# 			xl2=line[1][0]
# 			yl2=line[1][1]

# 			xl3=line[0][0]
# 			yl3=line[0][1]
# 			xl4=line[1][0]
# 			yl4=line[1][1]

# 			xl5=line[0][0]
# 			yl5=line[0][1]
# 			xl6=line[1][0]
# 			yl6=line[1][1]
			
# 			img = cv2.imread('Images/preview.jpg')
# 			cv2.line(img, line[0], line[1], (0, 255, 0), 3)
# 			cv2.imwrite('Images/copy.jpg', img)

# 			img = cv2.imread('./Images/preview.jpg')
# 			VideoFileOutput.write(img)
# 			#print('yola')
# 			frame=cv2.resize(image_np,(1020,647))
# 			cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
# 			img = Image.fromarray(cv2image)
# 			imgtk = ImageTk.PhotoImage(image=img)
# 			display1.imgtk = imgtk #Shows frame for display 1
# 			display1.configure(image=imgtk)
# 	window.config(cursor="plus")
# 	canvas=Canvas(master = window, width = 500, height = 500)
# 	canvas.bind("<Button-1>",imgclick)
	
	


#22222==========================================功能函数定义======================================
#33333==========================================加载检测模型区======================================
pool = ThreadPool(processes=1)
detection_graph = tf.Graph()
with detection_graph.as_default():
	od_graph_def = tf.GraphDef()
# tf.gfile模块的主要角色是：
# 1.提供一个接近Python文件对象的API，以及
# 2.提供基于TensorFlow C ++ FileSystem API的实现。
# 主要完成对文件的操作，各个函数参见https://blog.csdn.net/a373595475/article/details/79693430
with tf.gfile.GFile('Cars/output_inference_graph.pb', 'rb') as fid:
	serialized_graph = fid.read()
	od_graph_def.ParseFromString(serialized_graph)
	tf.import_graph_def(od_graph_def, name='')

# 得到各层参数
detection_graph=tf.get_default_graph()
#for op in detection_graph.get_operations():
#	print(op.name)

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


#cap=cv2.VideoCapture('Video/video-01.avi') # 0 stands for very first webcam attach
cap=cv2.VideoCapture('Video/input1.mp4')

#print(cap)
filename="testoutput.avi"
codec=cv2.VideoWriter_fourcc('m','p','4','v')#fourcc stands for four character code
framerate=10
resolution=(640,480)

VideoFileOutput=cv2.VideoWriter(filename,codec,framerate, resolution)
vs = WebcamVideoStream(src='Set01_video01.mp4').start()
ret,imgF=cap.read(0)
print(imgF)


imgF=Image.fromarray(imgF)

im_width, im_height = imgF.size
xl1=0
xl2=im_width-1 
#绿线
yl1=im_height*0.4 # input2
#yl1=im_height*0.9 # input1
#yl1=im_height*0.6 # video7
#yl1=im_height*0.8 # video-02
#yl1=im_height*0.8 # video-03
#yl1=im_height*0.9 # video-01

yl2=yl1
ml1=(yl2-yl1)/(xl2-xl1)

intcptl1=yl1-ml1*xl1


#(xl1,yl1)-(xl2,yl2):绿线，正常线；(xl3,yl3)-(xl4,yl4):蓝线，人行横道线；(xl5,yl5)-(xl6,yl6):红线，停车线
count=0
xl3=0
xl4=im_width-1
#红线
#yl3=im_height*0.3 # input2
yl3=im_height*0.8 # input1
#yl3=im_height*0.3 # video7
#yl3=im_height*0.65 # video-02
#yl3=im_height*0.65 # video-03
#yl3=im_height*0.65 #video-01
yl4=yl3
ml2=(yl4-yl3)/(xl4-xl3)

intcptl2=yl3-ml2*xl3

xl5=0
xl6=im_width-1
#蓝线
#yl5=im_height*0.2 # input2
yl5=im_height*0.7 # input1
#yl5=im_height*0.1 # video7
#yl5=im_height*0.5 # video-02
#yl5=im_height*0.5 # video-03
#yl5=im_height*0.5 # video-01

yl6=yl5
ml3=(yl6-yl5)/(xl6-xl5)
#ml3=0
intcptl3=yl5-ml3*xl5
ret=True
start=time.time()
c=0
sesser=tf.Session(graph=detection_graph)

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Each box represents a part of the image where a particular object was detected.
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Each score represent how level of confidence for each of the objects.
# Score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')
#print('这是主函数外的部分')
#33333==========================================加载检测模型区======================================
def main(sess=sesser):
	'''global masterframe
	global started'''
	#print('这里是main()函数')
	if True:
		fTime=time.time()
		_,image_np=cap.read(0)
		#image_np = imutils.resize(image_np, width=400)
		cv2.imwrite('Images/preview.jpg', image_np)
		# Definite input and output Tensors for detection_graph


		# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
		image_np_expanded = np.expand_dims(image_np, axis=0)
		# Actual detection.
		(boxes, scores, classes, num) = sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_np_expanded})


		# Visualization of the results of a detection.
		img=image_np
		imgF,coords=vis_util.visualize_boxes_and_labels_on_image_array(
			image_np,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			category_index,
			use_normalized_coordinates=True,
			line_thickness=2)
        
	
		matchVehicles(coords,im_width,im_height,imgF)
		checkRedLightCrossed(imgF)
		checkSpeed(fTime,img)
		for v in vehicles:
			if v.getTracking()==True:

				for p in v.getPoints():
					cv2.circle(image_np,p,3,(200,150,75),6)

			#print(ymin*im_height,xmin*im_width,ymax*im_height,xmax*im_width)
			#cv2.rectangle(image_np,(int(xmin*im_width),int(ymin*im_height)),(int(xmax*im_width),int(ymax*im_height)),(255,0,0),2)
		
		# 以下画出三条线：绿、蓝、红
		#print('line:{}'.format(line))
		
		cv2.line(image_np, (int(xl1),int(yl1)), (int(xl2),int(yl2)), (0,255,0),3)
		cv2.line(image_np, (int(xl3),int(yl3)), (int(xl4),int(yl4)), (0,0,255),3)
		cv2.line(image_np, (int(xl5),int(yl5)), (int(xl6),int(yl6)), (255,0,0),3)
		
		VideoFileOutput.write(image_np)
		#print('yola')
		frame=cv2.resize(image_np,(1020,647))
		cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		img = Image.fromarray(cv2image)

		#发送图片到后端
		#img2 = base64.b64encode(cv2image).decode()
		#image2 = []
		#image2.append(img2)
		#res = {"image":image2}
		#访问服务
		#_ = requests.post("http://192.168.137.70:5001",data=res)


		imgtk = ImageTk.PhotoImage(image=img)
		display1.imgtk = imgtk #Shows frame for display 1
		display1.configure(image=imgtk)
		#regionofinterest(window)
	window.after(1, main)

#44444==========================================可视化函数区======================================
window = tk.Tk()  #Makes main window
window.wm_title("战云智能交通监控系统--基于YOLO v3")
window.columnconfigure(0, {'minsize': 1020})
window.columnconfigure(1, {'minsize': 335})

#print('这里是窗口初始化的地方')
frame=tk.Frame(window)
frame.grid(row=0,column=0,rowspan=5,sticky='N',pady=10)

# 创建analyse()菜单,并添加命令。
#menu=Menu(window)
#window.config(menu=menu)
#analyse=Menu(menu)
#analyse.add_command(label="Region of Interest",command=regionofinterest)
#menu.add_cascade(label="Analyse",menu=analyse)

frame2=tk.Frame(window)
frame2.grid(row=0,column=1)

frame3=tk.Frame(window)
frame3.grid(row=1,column=1)

frame4=tk.Frame(window)
frame4.grid(row=2,column=1)

frame5=tk.Frame(window)
frame5.grid(row=3,column=1)

frame2.rowconfigure(1, {'minsize': 250})
frame3.rowconfigure(1, {'minsize': 80})
frame4.rowconfigure(1, {'minsize': 150})
frame5.rowconfigure(1, {'minsize': 80})

lbl1 = tk.Label(frame,text='Vehicle Detection And Tracking',font = "verdana 12 bold")
lbl1.pack(side='top')

lbl2 = tk.Label(frame2,text='Vehicle Breaking Traffic Rule',font = "verdana 10 bold")
lbl2.grid(row=0,column=0,sticky ='S',pady=10)

lbl3 = tk.Label(frame3,text='Veicle Speed',font = "verdana 10 bold")
lbl3.grid(row=0,column=0,sticky ='S',pady=10)

lbl4 = tk.Label(frame4,text='Detected License Plate',font = "verdana 10 bold")
lbl4.grid(row=0,column=0)

lbl5 = tk.Label(frame5,text='Extracted License Plate Number',font = "verdana 10 bold")
lbl5.grid(row=0,column=0)

display1 = tk.Label(frame)
display1.pack(side='bottom')  #Display 1

display2 = tk.Label(frame2)
display2.grid(row=1,column=0) #Display 2

display3 = tk.Label(frame3,text="",font = "verdana 14 bold",fg='red')
display3.grid(row=1,column=0)

display4 = tk.Label(frame4)
display4.grid(row=1,column=0)

display5 = tk.Label(frame5,text="",font = "verdana 24 bold",fg='green')
display5.grid(row=1,column=0)
masterframe=None
started= False
#44444==========================================可视化函数区======================================
'''thread = threading.Thread(target=stream)
thread.daemon = True
thread.start()'''
#55555==========================================可视化填充区======================================
with detection_graph.as_default():
	with tf.Session(graph=detection_graph) as sess:
		#print('这里是session')
		sesser=sess
		main(sess) #Display
window.mainloop()  #Starts GUI
#55555==========================================可视化填充区======================================
