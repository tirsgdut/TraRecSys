import requests
# from lxml import etree
# rsp = requests.get('https://guangzhou.8684.cn')
# if rsp.status_code == 200:
#     # bus_layer = '/html/body/div[6]/div[1]/div[4]/div/a'
#     bus_name = '//*[@id="con_site_1"]/a'
#     html = etree.HTML(rsp.text)
#     for i in html.xpath(bus_name):
#         print(i.text,i.get('href'))

url = 'https://map.baidu.com/?'
headers = {'Referer': '''https://map.baidu.com/search/1%E8%B7%AF/@12605568.38702564,2627977.4400000004,13.95z?querytype=s&da_src=shareurl&wd=1%E8%B7%AF&c=257&src=0&pn=0&sug=0&l=13&b=(12600151,2627495;12649303,2639239)&from=webmap&biz_forward=%7B%22scaler%22:2,%22styles%22:%22pl%22%7D&device_ratio=2''',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
params = {'qt': 'bsl',
 'tps': 'newmap: 1',
 'uid': 'a0a25b0223e487e1d0ff2384',	#修改你的id
 'c': '257'}
rsp = requests.get(url,params,headers=headers)
dict_ = rsp.json()

# 把字典里面的
# uid,name,station,timetable_ext,
#
# headway
#
# ,end_time
#
# ,sub-way
#数据拿出来