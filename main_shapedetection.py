import cv2
import numpy as np
import math
img = cv2.imread('test.jpg')


width = 500
height = int((width * img.shape[0])/img.shape[1])
dim = (width, height)
  
# resize image
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

_, thrash = cv2.threshold(img_gray,150,255,cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thrash,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)


for cnt in contours:
  #make Poly
  approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
  x = approx.ravel()[0]
  y = approx.ravel()[1]
  if len(approx) >10:
      ((x, y), r) = cv2.minEnclosingCircle(cnt)
      cv2.circle(img, (int(x), int(y)), int(r), (36, 255, 12), 2)
      line_thickness = 2
      x_1 = int(x-int(r))
      x_2 = int(x+int(r))
      cv2.line(img, (x_1, int(y)), (x_2,  int(y)), (255, 0, 0), thickness=line_thickness)
      x_text = int((x+x_2)/2)
      cv2.putText(img,'D:'+format(round(r*2,2)),(int((x +x_1)/2),int(y-5)),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255))
      print('Radius: {}'.format(r))


cv2.imshow("img",img)
cv2.imshow("shapes",thrash)
cv2.waitKey(0)
cv2.destroyAllWindows()