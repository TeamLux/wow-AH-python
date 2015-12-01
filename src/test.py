import json
from os import listdir
from os.path import join
from datetime import *
from wowObject import *
# use datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
path = join("..","results")
i = 0
files = sorted(listdir(path))
f = files[0]
date = datetime(year=1993,month=1,day=1,hour=0,minute=0,second=0)
datas = {}
for f in files:
	preDate = date
	preDatas = datas

	date = datetime(year=int(f[0:4]),month=int(f[4:6]),day=int(f[6:8]),hour=int(f[8:10]),minute=int(f[10:12]),second=int(f[12:14]))
	inter = date-preDate
	inter = int(inter.total_seconds())
	if inter > 5000:
		inter = 0

	f = join(path,f)
	print(date)

	f = open(f)
	data = json.load(f)
	datas={}
	for auction in data["auctions"]:
		if(auction["auc"] not in preDatas):
			datas[auction["auc"]]=WowObject(auction,date,inter)
		else:
			datas[auction["auc"]] = preDatas[auction["auc"]].update(auction,date)

	for auc in preDatas:
		if auc not in datas:
			if preDatas[auc].isBuy(date,inter)[0] is True:
				print("bid")
			elif preDatas[auc].isBuy(date,inter)[0] is False:
				print("NOT SELL")
			else:
				print("buy")
	i+=1
	print(i)
	f.close()

def load():
	pass