# -*- coding: utf-8 -*-
# @Time  : 2022/1/26 17:17
# @Author  : 呆呆
# @Email : 2821212670@qq.com
# @FileName  : test.py
# @Software  : PyCharm
import cv2;
import numpy as np


img = cv2.imread(r'D:\python\PaddleOCR-release-2.4\output\sdmgr_kie\kie_results\2.png');
rows=img.shape[0]
cols=img.shape[1]
channels=img.shape[2]
mask=np.zeros(img.shape,dtype=np.uint8)
#输入点的坐标
roi_corners=np.array([[(10,10),(40,20),(70,80),(5,100)]],dtype=np.int32)
channel_count=channels
ignore_mask_color = (255,)*channel_count
#创建mask层
cv2.fillPoly(mask,roi_corners,ignore_mask_color)
#为每个像素进行与操作，除mask区域外，全为0
masked_image=cv2.bitwise_and(img,mask)
cv2.imshow("src",masked_image)
cv2.waitKey(0)
