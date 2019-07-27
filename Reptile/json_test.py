import json

# 测试公交点
# with open('./data/bus/Info.json','rb') as f:    #需要在命令行调用
#     lst_ = json.load(f)[0]['stations']
# lst = [i['geo'][2:24] for i in lst_]

# *找到缺失的地铁路线*
#1.已爬取的路线
with open('./data/subways/Info.json','rb') as f:    #已爬取的文件
    lst_ = json.load(f)
l_name = []
l_uid = []
for tab in lst_:
    l_name.append(tab['name'][:5])  #前四个字
    l_uid.append(tab['uid'])

#2.地铁线名称
lst = []
with open('./data/subways/name.json', 'rb') as f:  # 需要在命令行调用
    lst_ = json.load(f)[0]["0"]
    for l in lst_:
        lst.append(l[:5]) #前四个字

# lst_c = lst[:]
# for i in lst_c: #变化
#     if i in l_name:
#         lst.remove(i)
print(lst)
# 通过对比，发现未爬取的路线均在err文件里