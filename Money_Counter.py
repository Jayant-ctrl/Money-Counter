import cv2
import cvzone
import numpy as np

url = 'http://192.168.213.31:81/stream'
capture = cv2.VideoCapture(url)

totalMoney = 0

# capture.set(3, 480)
# capture.set(4, 320)
def empty(a):
  pass

cv2.namedWindow("Settings")
cv2.resizeWindow("Settings",640,190)
cv2.createTrackbar("Threshold1", "Settings", 139, 255, empty)
cv2.createTrackbar("Threshold2", "Settings", 114, 255, empty)


def preProcessing(frame):
  imgPre = cv2.GaussianBlur(frame, (5,5), 3)
  thresh1 = cv2.getTrackbarPos("Threshold1", "Settings")
  thresh2 = cv2.getTrackbarPos("Threshold2", "Settings")
  imgPre = cv2.Canny(imgPre, thresh1, thresh2)   
  kernel = np.ones((3,3), np.uint8)
  imgPre = cv2.dilate(imgPre, kernel, iterations=1)
  imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CLOSE, kernel) 
  return imgPre

while True:
  isTrue, frame = capture.read()
  imgPre = preProcessing(frame)
  imgContours, conFound = cvzone.findContours(frame, imgPre, minArea=20)
  
  imgStack = cvzone.stackImages([imgPre, imgContours], 2, 1)
   
  totalMoney = 0 
  if conFound:
    for contour in conFound:
      peri = cv2.arcLength(contour['cnt'], True)
      approx = cv2.approxPolyDP(contour['cnt'], 0.02*peri, True)
     
      if(len(approx) > 5):
        area = contour['area']
        if area > 3100 and area < 3300 or area > 3300 and area <3350:
          totalMoney += 1
        elif area > 4600 and area <4910:
          totalMoney += 2       
        elif area > 5480 or area >5600:
          totalMoney += 10
  
  print(totalMoney)
  cvzone.putTextRect(imgStack, f'Rs.{totalMoney}', (50,50))
  cv2.imshow('Video', imgStack) 
#   cv2.imshow('Video',frame)
#   cv2.imshow('Pre', imgPre)
  cv2.waitKey(1)