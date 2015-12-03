import json
from os import listdir
from os.path import join
from datetime import *
from wowObject import *
from collections import defaultdict
from interStat import *
# use datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
# item = { 	QSale = int,
#			QBuy = int,
#  			inter ={Buy = {Q, MaxP, MinP, AvgP, StdP},
#					Sale = {Q, MaxP, MinP, AvgP, StdP},
#					upToSale={Q, MaxP, MinP, AvgP, StdP}
#			}
#}
# seller = {item = {QSale, QBuy}}

def load():
	pass

def save():
	pass

n12 = 0
n24 = 0
n48 = 0
n2448 = 0
nNone = 0
bid = 0
buy = 0
notBuy = 0

sellers = defaultdict(lambda :defaultdict(lambda: defaultdict(lambda :0)))
items = defaultdict(lambda: defaultdict(lambda :0))

interBuy = defaultdict(lambda: interStat())
interNotBuy = defaultdict(lambda: interStat())
interSale = defaultdict(lambda: interStat())
interUpToSale = defaultdict(lambda: interStat())

path = join("..","results")
i = 0
files = sorted(listdir(path))
f = files[0]
date = datetime(year=1993,month=7,day=31,hour=14,minute=26,second=20)
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
			datas[auction["auc"]] = WowObject(auction,date,inter)
			obj = datas[auction["auc"]]
			sellers[obj.owner][obj.item]["QSale"] += obj.quantity
			items[obj.item]["QSale"] += obj.quantity
			if obj.timeBegin != None:
				interUpToSale[obj.item].add(obj.buyout,obj.bid,obj.quantity)
		else:
			datas[auction["auc"]] = preDatas[auction["auc"]].update(auction,date)
		interSale[obj.item].add(obj.buyout,obj.bid,obj.quantity)

	for auc in preDatas:
		if auc not in datas:
			obj = preDatas[auc]
			res = obj.isBuy(date,inter)

			if obj.timeSell == 12:
				n12 +=1
			elif obj.timeSell == 24:
				n24 +=1
			elif obj.timeSell == 48:
				n48 +=1
			elif obj.timeSell == 2448:
				n2448 += 1
			else:
				nNone +=1

			if res != None:
				if isinstance(res,int):
					buy += 1
					sellers[obj.owner][obj.item]["QBuy"] += obj.quantity
					items[obj.item]["QBuy"] += obj.quantity
					interBuy[obj.item].add(obj.buyout,obj.bid,obj.quantity)
				elif res[0]:
					bid += 1
					sellers[obj.owner][obj.item]["QBuy"] += obj.quantity
					items[obj.item]["QBuy"] += obj.quantity
					interBuy[obj.item].add(obj.buyout,obj.bid,obj.quantity)
				else:
					notBuy += 1
					interNotBuy[obj.item].add(obj.buyout,obj.bid,obj.quantity)

	for key in interBuy:
		interBuy[key].save()
	for key in interNotBuy:
		interNotBuy[key].save()
	for key in interSale:
		interSale[key].save()
	for key in interUpToSale:
		interUpToSale[key].save()
	i+=1
	print(i)
	f.close()

