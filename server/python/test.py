# -*- coding:utf-8 -*-
from pymongo import Connection
import re
def juage(com,id,res_list,nushi):
	match = re.search(r'[_0-9]+',com)
	if match:
		#>>の文字があったら反映
		if match.start()-1>=0 and com[match.start()-1]=='>':
			res_list.append(int("".join(com[match.start():match.end()])))
			return 1,res_list
		#idがスレ主と同じだったら反映
	elif id==nushi:
		return 1,res_list
	return 0,res_list

def remove(data,nushi,nushi_res):
	out_dic={}
	res_list=[]
	for num in data.keys():
		boo,res_list=juage(data[num][1],data[num][0],res_list,nushi)
		if boo>0:
			out_dic[num]=data[num]
	for tar in res_list:
		out_dic[tar]=data[tar]
	return out_dic

def change(data_dic):
	out_list=[]
	for num in data_dic:
		s = str(num)+":ID"+data_dic[num][0]+"\n"+data_dic[num][1]
		print s
		out_list.append(s)
	return out_list


def DBconnect(col):
	for data in col.find():
		nushi = ""
		nushi_res = ""
		data_dic={'url':data['url']}
		res_dic={}
		tar_list = data['res']
		#タイトル
		title = data['title']
		data_dic['title']=title
		#レスの対象となったレスの番号リスト(>>0みたいな)
		for res_data in tar_list:
			res=res_data.split(u"：")
			#レスの番号
			if res[0]=="":
				break
			number = int(res[0])
			res = (res[2].split(u"ID:"))[1]
			#id
			id = (res.split(" "))[0]
			#レスの内容
			com = (" ").join((res.split(" "))[1:])
			res_dic[number]=[id,com]
			if number==1:
				nushi = id 
				nushi_res = com
		print nushi
		print nushi_res
		col.remove({'url':data['url']})
		print data_dic
		dic=remove(res_dic,nushi,nushi_res)
		res_out=change(dic)
		data_dic['res']=res_out
		col.insert(data_dic)

if __name__ == '__main__':
	con = Conneccon = Connection('mongodb://localhost/matome')
	
	#dbの選択
	db = con['matome']
	
	#collectionの選択
	col = db.matomedbs
	out = db.out
	while 1:
		DBconnect(col)

