import cv2
import numpy as np
import math
img = cv2.imread('test.jpg', -1)

rgb_planes = cv2.split(img)

edge_planes = []
# result_norm_planes = []
for plane in rgb_planes:
    dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(plane, bg_img)
    norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    edge_planes.append(diff_img)
    # result_norm_planes.append(norm_img)

edge = cv2.merge(edge_planes)




# 灰色
img_gray = cv2.cvtColor(edge,cv2.COLOR_BGR2GRAY)

img_gray = 255 - img_gray


_, thrash = cv2.threshold(img_gray,35,255,cv2.THRESH_BINARY)

# Copy the thresholded image
im_floodfill = thrash.copy()

# Mask used to flood filling.
# NOTE: the size needs to be 2 pixels bigger on each side than the input image
h, w = thrash.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

# Floodfill from point (0, 0)
cv2.floodFill(im_floodfill, mask, (0,0), 255)

# Invert floodfilled image
im_floodfill_inv = cv2.bitwise_not(im_floodfill)

# Combine the two images to get the foreground
im_out = thrash | im_floodfill_inv

contours, _ = cv2.findContours(im_out,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

#計算圓形 與算直徑
for cnt in contours:
  #make Poly
  approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
  x = approx.ravel()[0]
  y = approx.ravel()[1]
  if len(approx) >10:
      ((x, y), r) = cv2.minEnclosingCircle(cnt)
      cv2.circle(img, (int(x), int(y)), int(r), (36, 255, 12), 1)
      line_thickness = 1
      x_1 = int(x-int(r))
      x_2 = int(x+int(r))
      cv2.line(img, (x_1, int(y)), (x_2,  int(y)), (255, 0, 0), thickness=line_thickness)
      x_text = int((x+x_2)/2)
      cv2.putText(img,'D:'+format(round(r*2,2)),(int((x +x_1)/2),int(y-5)),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255))
      print('Radius: {}'.format(r))
      #cv2.drawContours(img,[approx],0,(255,0,0),2)


cv2.imshow("img",img)
cv2.imshow("edge",edge)
cv2.imshow("img_gray",img_gray)
cv2.imshow("shapes",im_out)
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite('./shadow_test/shadow_out.jpg', result)
# cv2.imwrite('./shadow_test/shadow_nor_test.jpg', result_norm)

