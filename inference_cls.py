# -*- coding: utf-8 -*-
# @Time  : 2022/3/10 15:35
# @Author  : 呆呆
# @Email : 2821212670@qq.com
# @FileName  : inference_cls.py
# @Software  : PyCharm
import os

from serving.ocr_cls.module import OCRCls

import uvicorn
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel


class Item(BaseModel):
    file_list: list


ocr = OCRCls()

app = FastAPI(title='Hello world')


def read_directory(directory_name):
    image_list = []
    for root, dirs, files in os.walk(directory_name):
        # for dir in dirs:
        # print(os.path.join(root,dir))
        for file in files:
            # print(os.path.join(root,file))
            image_list.append(os.path.join(root, file))
    return image_list


# image_path = [
#     r'D:\python\PaddleOCR-release-2.4\1.jpg'
#
# ]

@app.post('/dection_inverted', summary='ocr')
async def dection_inverted(item: Item):
    all_res=[]
    for i in item.file_list:
        image_path = read_directory(i)
        res = ocr.predict(paths=image_path)
        all_res.append(res)
    print(all_res)

    return {"code": 0, "result": all_res}


if __name__ == "__main__":
    uvicorn.run(app, debug=True, host='127.0.0.1')
