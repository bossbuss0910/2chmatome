# -*- coding:utf-8 -*-
from pymongo import Connection
import re
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
	#レスの対象となったレスの番号リスト(>>0みたいな)
	tar_list=[]
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
		if number==1:
			data_dic['res'][number]=[id,com]
			nushi = id 
			nushi_res = com
		else:
			match = re.findall(r'[0-9]+',com)
			if len(match)>0:
				if com.find('>>'):
					data_dic['res'][number]=[id,com]
			elif id==nushi:
				data_dic['res'][number]=[id,com]
	print nushi
	print nushi_res
#	col.remove({'url':data['url']})
	print data_dic
	out.insert(data_dic)
