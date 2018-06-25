# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 10:15:08 2017

@author: jhs
"""

def addconvert():
    import os
    import numpy as np
    import pandas as pd
    

    file_path = os.path.split(os.path.realpath('__file__'))[0]
    sys_card_area = pd.read_csv(file_path + "\sys_card.csv",encoding = 'gb18030')
    print(sys_card_area.head())



#
#sys_card_area = sys_card_area[['card_no','address','province','city','area']]
#
## 省
#id_province = sys_card_area[['card_no','province']]
#id_province.set_index('card_no',inplace = True)
#province_dict = list(id_province.to_dict(orient = 'dict').values())[0]
#
## 市
#id_city = sys_card_area[['card_no','city']]
#id_city.set_index('card_no',inplace = True)
#city_dict = list(id_city.to_dict(orient = 'dict').values())[0]
#
## 区/县
#id_area = sys_card_area[['card_no','area']]
#id_area.set_index('card_no',inplace = True)
#area_dict = list(id_area.to_dict(orient = 'dict').values())[0]

# 删除中间表，减少占用资源
#del id_province
#del id_city
#del id_area

# 使用方法
# id_address['province'] = id_address['area_code'].map(province_dict)
