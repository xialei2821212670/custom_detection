# -*- coding: utf-8 -*-
# @Time  : 2022/2/23 15:42
# @Author  : 呆呆
# @Email : 2821212670@qq.com
# @FileName  : server.py
# @Software  : PyCharm
# -*- coding: utf-8 -*-
# @Time  : 2022/2/15 14:23
# @Author  : 呆呆
# @Email : 2821212670@qq.com
# @FileName  : web_server.py
# @Software  : PyCharm
import os
import random
import shutil
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

import aiofiles
import uvicorn
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pdf2image import convert_from_path


sys.path.append('../')

import layoutparser as lp
import cv2
from serving.module import OCRSystem


# import visualization as lp

class Item(BaseModel):
    file_list: list


app = FastAPI(title='Hello world')

save_dir = "/home/ub/Project/custom_detection/upload/"
URL ="https://mp.kunjuee.com:7020/"

# load model
# model = lp.PaddleDetectionLayoutModel(model_path=r"D:\python\custom_detection\ppyolo\inference\ppyolov2_r50vd_dcn_365e_coco",
#                                       threshold=0.5,
#                                       label_map={0: "_background_", 1: "Text", 2: "Title", 3: "Figure",
#                                                  4: "Figure caption", 5: "Table", 6: "Table caption",
#                                                  7: "Header", 8: "Footer", 9: "Reference", 10: "Equation"
#                                                  },
#                                       enforce_cpu=False,
#                                       enable_mkldnn=True,
#                                       thread_num=12)
ocr = OCRSystem()
model = lp.PaddleDetectionLayoutModel(model_path='./ppyolo/ppyolov2_r50vd_dcn_365e_coco',
                                      threshold=0.5,
                                      label_map={0: "header", 1: "reference_number", 2: "straight_matter", 3: "content",
                                                 4: "provenance", 5: "date"
                                                 },
                                      enforce_cpu=True,
                                      enable_mkldnn=True,
                                      thread_num=12)


# detect

# all_types = set([b.type for b in layout if hasattr(b, "type")])
# print("all_types", all_types)

# show_img.show()

def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def pdf_to_image(pdf_file):
    savefile =save_dir+ generate_random_str+".jpg"
    images = convert_from_path(pdf_path=pdf_file, dpi=300,

                               )
    # imag_file = r"D:\python\web_fastapi\demo\\"
    # page.save(imag_file + "0001" + '.jpg', 'JPEG')
    images[0].save(savefile, 'JPEG')
    return savefile


async def upload_image(file: UploadFile = File(...)):
    file_list = []
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")


    if file.filename.split(".")[-1]  =="pdf":
        async with aiofiles.open(file.content_type.split('/')[1], 'wb') as f:
            content = await file.read()  # async read
            await f.write(content)
            tmp_file_name = pdf_to_image(file.content_type.split('/')[1])


    if  extension :
        # return "Image must be jpg or png format!"
        try:
            suffix = Path(file.filename).suffix

            with NamedTemporaryFile(delete=False, suffix=suffix, dir=save_dir) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_file_name = Path(tmp.name).name

        finally:
            file.file.close()
            file_list.append(tmp_file_name)
    return file_list




@app.post('/Layout_image', summary='ocr')
async def Layout_ocr_api(file: UploadFile = File(...)):
    file_list = await upload_image(file)

    for file_image in file_list:
        image = cv2.imread(save_dir +file_image)
        image = image[..., ::-1]
        layout = model.detect(image)

        # print(layout)
        # show result
        # show_img = lp.draw_box_show(image, layout, box_width=3, show_element_type=True)
        # show_img.show()  # 展示全部检测结果

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

        # show_img.show()  # 展示获取到的区域
        # print("header", text_blocks)

        print("接收参数:", visualization_res)

        for i in range(len(visualization_res)):
            x_1 = int(visualization_res[i]['x_1'] - 10)
            y_1 = int(visualization_res[i]['y_1'] - 10)
            x_2 = int(visualization_res[i]['x_2'] + 10)
            y_2 = int(visualization_res[i]['y_2'] + 10)
            dst = image[y_1:y_2, x_1:x_2]
            dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
            # cv2.imshow("test", dst)
            # cv2.waitKey(0)

            image_path = [dst
                          # './doc/imgs/11.jpg',
                          # './doc/imgs/12.jpg',
                          ]
            res = ocr.predict(images=image_path)
            print(res)
    return {"code": 0, "result": res,"url":URL+file_image}



if __name__ == "__main__":
   # uvicorn.run(app, debug=True, host='127.0.0.1')
    uvicorn.run(app, debug=True, host='0.0.0.0', port=9281)
