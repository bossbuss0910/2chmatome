# -*- coding:utf-8 -*-
from pymongo import Connection
import re
import time

#反映するかどうかの判定
def juage(com,id,res_list,nushi):
	match = re.search(r'[_0-9]+',com)
	if match:
		#>>の文字があったら反映
		if match.start()-1>=0 and com[match.start()-1]=='>':
			res_list.append(int("".join(com[match.start():match.end()])))
			return int("".join(com[match.start():match.end()])),res_list
	#idがスレ主と同じだったら反映
	elif id==nushi:
		res_list.append(1)
		return 0,res_list
	return 0,res_list

#データ構造を作る
def remove(data,nushi,nushi_res):
	out_dic={}
	fire_dic={}
	res_list=[]
	for num in data.keys():
		boo,res_list=juage(data[num][1],data[num][0],res_list,nushi)
		if boo>0:
			data[num][1] = data[num][1].replace(' ', '<br>')
			if boo not in out_dic.keys():
				out_dic[boo]={}
				out_dic[boo][num]=data[num]
			else:
				out_dic[boo][num]=data[num]
	for tar in res_list:
		if tar<999:
			fire_dic[tar]=data[tar]
	return out_dic,fire_dic

#流れを作る
def change(data_dic,out_dic):
	print data_dic
	out_list=[]
	#発火を反映
	for num in sorted(data_dic.keys()):
		s = str(num)+":ID"+data_dic[num][0]+"<br><font size=\"5\" color=\"#ff0000\">"+data_dic[num][1]+"</font>"
		print s
		out_list.append(s)
		#ターゲットの後にそのあとの返事を反映
		if num in out_dic.keys():
			for res in sorted(out_dic[num].keys()):
				if res not in data_dic.keys():
					s = str(res)+":ID"+out_dic[num][res][0]+"<br>"+out_dic[num][res][1]
					print s
					out_list.append(s)
	return out_list


def DBconnect(col,out):
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
			print res[0]
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
		o_dic,f_dic=remove(res_dic,nushi,nushi_res)
		res_out=change(f_dic,o_dic)
		data_dic['res']=res_out
		print data_dic
		out.insert(data_dic)

if __name__ == '__main__':
	con = Conneccon = Connection('mongodb://localhost/matome')
	
	#dbの選択
	db = con['matome']	
	#collectionの選択
	col = db.matomedbs
	outs = db.outs
	while 1:
		DBconnect(col,outs)

