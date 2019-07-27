# -*- coding: utf-8 -*-
import scrapy
import random
import json
import re

lst = []
def get_uid_lst(file='./data/bus/uid.json'):
    with open(file, 'rb') as f:  # 需要在命令行调用
        lst_ = json.load(f)
    lst = []
    for l in lst_:  # 第一个分类的点
        if len(l["0"]) == 2:
            lst.extend(l["0"])  #[0]
    return lst
input(lst)
# lst = get_uid_lst()  #地铁数据
# lst = lst[:-1]

#地铁数据
lst = get_uid_lst('./data/subways/uid.json')[:-1]

#url = 'http://map.baidu.com/?qt=bsl&tps=newmap%3A+1&uid={}&c=257'  #公交
url = 'https://map.baidu.com/?qt=bsl&tps=&newmap=1&uid={}&c=257'    #地铁
class LineinfoSpider(scrapy.Spider):
    start_urls = ['http://map.baidu.com/?qt=bsl&tps=newmap%3A+1&uid=9acf635503a5bc5cbc484251&c=257']    #公交
    #start_urls = ['http://map.baidu.com/?qt=bsl&tps=newmap%3A+1&uid=d918c70eb10d0c7302897283&c=257']    #地铁

    def parse(self, response):
        info = {}
        try:
            text = json.loads(response.body_as_unicode())['content'][0]
            #提取信息
            info['uid'] = text['uid']
            info['name'] = text['name']
            # info['stations'] = text['stations']
            # 深拷贝
            # input(type(text['stations']))
            a = text['stations'][:]
            # input(a)
            info['timetable_ext'] = text['timetable_ext']
            try:
                info['headway'] = text['headway']
            except:
                info['headway'] = None
            info['endTime'] = text['endTime']
            # print(text)
            # print(text['stations'])
            # 将途径站的信息转化
            # input(info['stations'])

            delect = ['pre_open', 'rt_info', 'tri_rt_info']
            # 遍历每一个字典
            for i in range(len(text['stations'])):
                # input(len(text['stations']))
                keys = list(text['stations'][i].keys())
                for key in keys:
                    if key in delect:
                        # 删除无用的键；
                        del (a[i][key])
                    if key == 'subways':
                        str = re.sub("[A-Za-z\"\#\=\<\>\/]", "", text['stations'][i][key][0]['name'])
                        a[i][key] = str

            info['stations'] = a
            yield info
        except:
            with open('error_s_info.txt', 'a') as f:
                f.write(response.url+'\n')
        if lst:
            yield scrapy.Request(url.format(lst.pop()),self.parse,dont_filter=True)

#scrapy crawl lineInfo -o ./data/subways/Info.json
#scrapy crawl lineInfo -o ./data/bus/Info.json