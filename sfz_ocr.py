# -*- coding: utf-8 -*-
# @Time  : 2022/3/5 9:07
# @Author  : 呆呆
# @Email : 2821212670@qq.com
# @FileName  : sfz_ocr.py
# @Software  : PyCharm
import cv2

from serving.module import OCRSystem
ocr = OCRSystem()

image = cv2.imread(r'C:\Users\admin\Desktop\sfz.jpg')
image = image[..., ::-1]
image_path = [image
              # './doc/imgs/11.jpg',
              # './doc/imgs/12.jpg',
              ]
res = ocr.predict(images=image_path)
print(res)
