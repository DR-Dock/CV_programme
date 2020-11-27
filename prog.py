import cv2
import sys
import os
import numpy as np

def makeVideo(dirr):
  names = []
  dirr = dirr + '/'
  files = os.listdir(dirr) 
  for x in range(len(files)-1):
    names.append(dirr+str(x)+'.jpg')
    

  frame = cv2.imread(names[0])  
  writer = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'), 
    25.0,  
    (frame.shape[1], frame.shape[0]),
    isColor=len(frame.shape) > 2)
  for frame in map(cv2.imread, names):
    writer.write(frame)
  writer.release()
  cv2.destroyAllWindows()
  

def main(cap):
  cap.set(3,1280) 
  cap.set(4,700)
  
  ret, frame1 = cap.read()
  ret, frame2 = cap.read()

  while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2) 
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) 
    dilated = cv2.dilate(thresh, None, iterations = 3) 
    сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    for contour in сontours:
      (x, y, w, h) = cv2.boundingRect(contour) 
     
      if cv2.contourArea(contour) < 700: 
        continue
     
      cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2) 
      cv2.putText(frame1, " {},{}".format(x,y), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA) 
   
    cv2.imshow("frame1", frame1)
    frame1 = frame2  #
    ret, frame2 = cap.read() #  
    if cv2.waitKey(40) == 27:
      break
   
  cap.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
 
  print("1 - камера устройства")
  print("2 - видеофайл")
  print("3 - Набор изображений")
  option = input("выберите источник кадров:")
  if option == '1':
    cap = cv2.VideoCapture(0)
    main(cap)
  elif option == '2':
    f = input("имя видеофайла:")
    cap = cv2.VideoCapture(f)
    main(cap)
  elif option == '3':
    dirr = input("папка с кадрами:")
    makeVideo(dirr)
    cap = cv2.VideoCapture('output.avi')
    main(cap)

