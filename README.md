# opencv_reshadow

在電腦上的圖片不會產生影子、對比度高，但在現實中影子無處不在，以致增加偵測困難，
所以必須先處理影子問題，才能提高判斷準確度

- 電腦圖片
<img src="computer.jpg" width="250" title="hover text">

- 現實情況
<img src="test.jpg" width="250" title="hover text">

## 原先結果
<img src="./img/result_01.jpg" width="350" title="hover text">


## 處裡方式

- 抓取邊緣

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

<img src="./img/removeshadow_01.jpg" width="250" title="hover text">

- 轉成灰階並反轉

      img_gray = cv2.cvtColor(edge,cv2.COLOR_BGR2GRAY)
      img_gray = 255 - img_gray


<img src="./img/removeshadow_02.jpg" width="250" title="hover text">
