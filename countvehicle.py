import cv2
import numpy as np
import sys

cam=cv2.VideoCapture('data/street.mov')
#cam=cv2.VideoCapture('data/pisang-topi.mov')
#cam=cv2.VideoCapture('data/traffic.avi')
#cam=cv2.VideoCapture('data/vtrain1.mp4')
#cam=cv2.VideoCapture(0)

#fgbg = cv2.BackgroundSubtractorMOG()

_, fo = cam.read()
framei = cv2.cvtColor(fo, cv2.COLOR_BGR2GRAY)
bg_avg = np.float32(framei)

#reset capture
cam.release()
cam=cv2.VideoCapture('data/street.mov')
#cam=cv2.VideoCapture('data/pisang-topi.mov')
#cam=cv2.VideoCapture('data/traffic.avi')
#cam=cv2.VideoCapture('data/vtrain1.mp4')
#cam=cv2.VideoCapture(0)

#Variabel Kwalitas Tracking

video_width = int(cam.get(3))
video_height = int(cam.get(4))

waktu_muat = 0.01
blur_level = 35
besar_obj = 100
thresh_level = 30
cnt_i = 0
jml_kendaraan = 0

stop_hitung = {}
stop_hitung[cnt_i] = 0
posisi_hitung = {}
posisi_hitung[cnt_i] = 0

while(cam.isOpened): 
	f,img=cam.read()
	
	if f==True:
       #img=cv2.flip(img,1)
       #img=cv2.medianBlur(img,3)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		
		#extract background
		cv2.accumulateWeighted(gray, bg_avg, waktu_muat)
		
		res1 = gray
                   
		res1 = cv2.absdiff(gray, cv2.convertScaleAbs(bg_avg))
		blur = cv2.GaussianBlur(res1,(blur_level,blur_level),0)	
		#gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
		#fgmask = fgbg.apply(gray)
		#blur = cv2.GaussianBlur(fgmask,(25,25),0)
		#thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
		
		
		#fgmask = fgbg.apply(thresh)
		#fgmask = fgbg.apply(gray)
		erode = cv2.erode(blur, None,iterations=2)
		dilate = cv2.dilate(erode, None, iterations=5)
		ret, thresh = cv2.threshold(dilate, thresh_level, 255, cv2.THRESH_BINARY)
		#contours,hierarchy = cv2.findContours(fgmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) cv2.RETR_EXTERNAL
		contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.line(
        
		
		
		for cnt in contours:
			
			cnt_i+=1
			#Buat Garis batas
			cv2.rectangle(img,(video_width,0),(video_width,500),(255,255,255),2)
			cv2.line(img,(video_width/4,0),(video_width/4, video_height),(0,0,255),2)
			cv2.line(img,(video_width/2,0),(video_width/2, video_height),(0,0,255),2)
			
			#hitung luas contour
			area = cv2.contourArea(cnt)
			#center_text = str(cnt_i)
			#pnj_karakter = len(center_text)/2 
			
			if area >= besar_obj: 
				#buat mark ditengah rectangle
				(cx,cy),radius = cv2.minEnclosingCircle(cnt)				
				cv2.circle(img,(int(cx),int(cy)),8,(0,0,255),-1)
				#if cx <
				tampil = 'x = ',str(cx), 'y = ',str(cy), 'area = ', str(area)
				#print tampil
				center_text = str(area)
				batas_hitung = int(video_width/4)
				posisi_object = int(cx)
				
				if posisi_object <= batas_hitung: 					
					posisi_hitung[cnt_i]=1
					stop_hitung[cnt_i]=0
				elif posisi_object > batas_hitung: 
					posisi_hitung[cnt_i]=0
					stop_hitung[cnt_i]=0
				
				#print 'posisi :',posisi_object, 'posisi_hitung: %s' %cnt_i, posisi_hitung[cnt_i], 'stop_hitung: %s' %cnt_i, stop_hitung[cnt_i]
				
				if (posisi_hitung[cnt_i]==1) & (stop_hitung[cnt_i]==0): 
					cv2.line(img,(video_width/4,0),(video_width/4, video_height),(0,255,0),10)
					jml_kendaraan +=1
					stop_hitung[cnt_i]=1
					print '############# --- Hitung Lagi --- ##############'
					print 'posisi :',posisi_object, 'posisi_hitung: %s' %cnt_i, posisi_hitung[cnt_i], 'stop_hitung: %s' %cnt_i, stop_hitung[cnt_i]
				
				#cv2.circle(img,(int(cx),int(cy)),radius,(0,0,255),2)
				#cx = centroid_x dan cy = centroid_y
				
				#buat rectangle
				#rect = cv2.minAreaRect(cnt)
				#print rect
				#box = cv2.boxPoints(rect)
				#box = np.int0(box)
				#cv2.drawContours(img,[box],0,(0,0,255),2)
				
				
				[x,y,w,h] = cv2.boundingRect(cnt)
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
				
				#cv2.rectangle(img,(((x+w)/2),((y+h)/2)),(x+w,y+h),(0,0,255),2)
				#cv2.putText(img,area,((int(cx)+2),(int(cy+2)), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0)))
				#JENIS FONT
				#FONT_HERSHEY_COMPLEX
				#FONT_HERSHEY_COMPLEX_SMALL
				#FONT_HERSHEY_DUPLEX
				#FONT_HERSHEY_PLAIN
				#FONT_HERSHEY_SCRIPT_COMPLEX
				#FONT_HERSHEY_SCRIPT_SIMPLEX
				#FONT_HERSHEY_SIMPLEX
				#FONT_HERSHEY_TRIPLEX
				#FONT_ITALIC
				cv2.putText(img,center_text, ((int(cx)+2),(int(cy+5))), cv2.FONT_HERSHEY_DUPLEX, 2, 255)
				cv2.putText(img,str(jml_kendaraan), (int(video_width/4),100), cv2.FONT_HERSHEY_DUPLEX, 3, 255)
				
		cv2.imshow('ASLI',img)
		#cv2.imshow('erode',erode)
		#cv2.imshow('dilate',dilate)
		#cv2.imshow('fgmask',fgmask)       

		#cv2.imshow('Grey',gray)		
		#cv2.imshow('blur',blur)
		cv2.imshow('thresh',thresh)
		
	k = cv2.waitKey(20)
	if(k == 27):
		break
	   
cam.release()
cv2.destroyAllWindows()
sys.exit()
