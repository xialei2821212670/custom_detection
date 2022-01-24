# -*- coding: utf-8 -*-
# @Time  : 2022/1/22 11:09
# @Author  : 呆呆
# @Email : 2821212670@qq.com
# @FileName  : data_list.py
# @Software  : PyCharm

res = [{'id': '0', 'type': 'Title', 'x_1': 135.47334, 'y_1': 407.1395, 'x_2': 298.02966, 'y_2': 431.44516,
        'score': 0.9624675},
       {'id': '1', 'type': 'Title', 'x_1': 136.12622, 'y_1': 461.43747, 'x_2': 340.29678, 'y_2': 481.20718,
        'score': 0.9397268},
       {'id': '2', 'type': 'Title', 'x_1': 651.462, 'y_1': 321.9767, 'x_2': 943.4111, 'y_2': 341.619,
        'score': 0.9411994},
       {'id': '3', 'type': 'Title', 'x_1': 649.2716, 'y_1': 1161.7778, 'x_2': 919.6543, 'y_2': 1181.4021,
        'score': 0.94586486}]

for i in range(len(res)):
    print(res[i]['x_1'])
    print(res[i]['type'])
    print(res[i]['score'])

