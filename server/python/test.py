# -*- coding:utf-8 -*-
from pymongo import Connection

con = Connection('mongodb://localhost/matome')

#dbの選択
db = con['matome']

#collectionの選択
col = db.matomedbs
out = db.out

for data in col.find():
	nushi = ""
	nushi_res = ""
	data_dic={'url':data['url'],'res':{}}
	tar_list = data['res']
	#タイトル
	title = data['title']
	data_dic['title']=title
	for res_data in tar_list:
		res=res_data.split(u"：")
		#レスの番号
		if res[0]=="":
			break
		number = int(res[0])
		print number
		res = (res[2].split(u"ID:"))[1]
		#id
		id = (res.split(" "))[0]
		print id
		#レスの内容
		com = (" ").join((res.split(" "))[1:])
		print com
		data_dic['res'][number]=[id,com]
		if number==1:
			nushi = id 
			nushi_res = com
	print nushi
	print nushi_res
	col.remove({'url':data['url']})
	print data_dic
	out.insert(data_dic)
