# -*- coding: utf-8 -*-
# @Time  : 2022/1/21 10:03
# @Author  : 呆呆
# @Email : 2821212670@qq.com
# @FileName  : inference.py
# @Software  : PyCharm

import sys

sys.path.append('../')

import layoutparser as lp
import cv2
from serving.module import OCRSystem

# import visualization as lp


image = cv2.imread(r'C:\Users\admin\Desktop\0084.jpg')
image = image[..., ::-1]

# load model
# model = lp.PaddleDetectionLayoutModel(model_path=r"D:\python\Tabel_ocr\inference\ppyolov2_r50vd_dcn_365e_coco",
#                                       threshold=0.5,
#                                       label_map={0: "_background_", 1: "Text", 2: "Title", 3: "Figure",
#                                                  4: "Figure caption", 5: "Table", 6: "Table caption",
#                                                  7: "Header", 8: "Footer", 9: "Reference", 10: "Equation"
#                                                  },
#                                       enforce_cpu=False,
#                                       enable_mkldnn=True,
#                                       thread_num=12)

model = lp.PaddleDetectionLayoutModel(model_path=r"D:\python\custom_detection\ppyolo\ppyolov2_r50vd_dcn_365e_coco",
                                      threshold=0.5,
                                      label_map={0: "header", 1: "reference_number", 2: "straight_matter", 3: "content",
                                                 4: "provenance", 5: "date"
                                                 },
                                      enforce_cpu=False,
                                      enable_mkldnn=True,
                                      thread_num=12)


# detect
layout = model.detect(image)

# print(layout)
# show result
show_img = lp.draw_box_show(image, layout, box_width=3, show_element_type=True)
show_img.show()  #展示全部检测结果
# all_types = set([b.type for b in layout if hasattr(b, "type")])
# print("all_types", all_types)

# show_img.show()

text_blocks = lp.Layout([b for b in layout if b.type == 'header'])
figure_blocks = lp.Layout([b for b in layout if b.type == 'date'])

# text areas may be detected within the image area, delete these areas
text_blocks = lp.Layout([b for b in text_blocks \
                        ])

# sort text areas and assign ID
h, w = image.shape[:2]

left_interval = lp.Interval(0, w / 2 * 1.05, axis='x').put_on_canvas(image)

left_blocks = text_blocks.filter_by(left_interval, center=True)
left_blocks.sort(key=lambda b: b.coordinates[1])

right_blocks = [b for b in text_blocks if b not in left_blocks]
right_blocks.sort(key=lambda b: b.coordinates[1])

# the two lists are merged and the indexes are added in order
text_blocks = lp.Layout([b.set(id=idx) for idx, b in enumerate(left_blocks + right_blocks)])

# print("text_blocks1", text_blocks)
# display result
show_img, visualization_res = lp.draw_box(image, text_blocks,
                                          box_width=3,
                                          show_element_id=True, show_element_type=True)

show_img.show()  #展示获取到的区域
print("header", text_blocks)

print("接收参数:", visualization_res)
ocr = OCRSystem()

for i in range(len(visualization_res)):
    x_1 = int(visualization_res[i]['x_1'] - 10)
    y_1 = int(visualization_res[i]['y_1'] - 10)
    x_2 = int(visualization_res[i]['x_2'] + 10)
    y_2 = int(visualization_res[i]['y_2'] + 10)
    dst = image[y_1:y_2, x_1:x_2]
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    cv2.imshow("test", dst)
    cv2.waitKey(0)

    image_path = [dst
                  # './doc/imgs/11.jpg',
                  # './doc/imgs/12.jpg',
                  ]
    res = ocr.predict(images=image_path)
    print(res)

# show_img.show()
