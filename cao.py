# import urllib.parse
import pandas as pd
import requests
# import math
# import time 
# import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import date

def function_crawl():
    df = pd.DataFrame(columns=['name', 'district', 'price', 'bedroom', 'wc', 'acreage', 'link', 'date'])
    i = 1
    while True: 
        link_root = 'https://mogi.vn/ho-chi-minh/mua-nha?cp='+str(i)
        response = requests.get(link_root)
        soup = BeautifulSoup(response.content, 'html.parser')   

        content0 = soup.find('ul', class_ = 'props').find_all('a', class_ = 'link-overlay') 
        content1 = soup.find_all('div', class_ = 'prop-addr')
        content2 = soup.find_all('div', class_ = 'price')
        content3 = soup.find_all('ul', class_ = 'prop-attr')
        content4 = soup.find_all('h2', class_ = 'prop-title')
        content5 = soup.find_all('div', class_ ='prop-created')
        if len(content5) == 0: break
        for x, y, z, t, u, v in zip(content0, content1, content2, content3, content4, content5):
            link = x.get('href')
            district = y.text
            price = z.text
            tmp = t.text.strip().split('\n')
            bedroom, wc, acreage = tmp[1], tmp[2], tmp[0]
            name = u.text
            day = v.text
            new_row = pd.Series([name, district, price, bedroom, wc, acreage, link, day], index=df.columns)
            df.loc[len(df)] = new_row
        
        print('page:', i)
        i += 1
    print('sl page: ', len(df))
    df.to_csv('/data/house_full.csv',index=None)

#------------- crawl infor----------- 
    dic = {'Diện tích sử dụng': 'area_used', 'Diện tích đất': 'area', 'Phòng ngủ': 'bedroom', 'Nhà tắm': 'wc', 'Pháp lý': 'juridical', 'Ngày đăng': 'date_submitted', 'Mã BĐS': 'id'}
    dic_df = {'id': '', 'area_used':'', 'area': '', 'bedroom': '', 'wc': '', 'juridical': '', 'date_submitted': ''}
    df_info = pd.DataFrame(columns=['id', 'area_used', 'area', 'bedroom', 'wc', 'juridical', 'date_submitted', 'link', 'address', 'latitude', 'longitude', 'describe', "seller", "seniority", "phone", "link_seller"])
    
    cc = 0
    for link in df['link']:
        dic_df = {'id': '', 'area_used':'', 'area': '', 'bedroom': '', 'wc': '', 'juridical': '', 'date_submitted': ''}
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        try: address = soup.find('div', class_ = 'address').text
        except: address = ''
        info = soup.find_all('div', class_ = 'info-attr clearfix')
        for i in info:
            tmp = i.text.strip().split('\n')
            dic_df[dic[tmp[0]]] = tmp[1]
        try: describe = soup.find('div', class_ = 'info-content-body').text
        except: describe = ''
        try:
            lat_long = soup.find('div', class_ = 'map-content clearfix').find('iframe').get('data-src').split('=')[-1].split(',')
            latitude = lat_long[0]
            longitude = lat_long[1]
        except: latitude, longitude = '', ''
        try: seller_name = soup.find('div', class_ = 'agent-name').text.replace('\n', '').replace('\r', '').strip()
        except: seller_name = ''
        try: seniority = soup.find('div', class_ = 'agent-date').text.replace('Đã tham gia: ', '')
        except: seniority = ''
        try: phone = soup.find('div', class_ = 'agent-contact clearfix').find('span').text.strip(' ')
        except: phone = ''
        try: 
            seller = soup.find('div', class_ = 'agent-name').find('a').get('href')
            link_seller = 'https://mogi.vn' + seller
        except:
            link_seller = ''

        arr = []
        for ii in dic_df.keys(): arr.append(dic_df[ii])
        arr.extend([link, address, latitude, longitude, describe])
        arr.extend([seller_name, seniority, phone, link_seller])

        new_row = pd.Series(arr, index=df_info.columns)
        df_info.loc[len(df_info)] = new_row

        cc += 1
        print('link:',cc)
    df_info.to_csv('/data/house_info_full.csv',index=None)

function_crawl()


