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
global n12,n24,n48,n2448,nNone,bid,buy,notBuy,sellers,items,startID,datas,date,ID

def load():
	global n12,n24,n48,n2448,nNone,bid,buy,notBuy,sellers,items,startID,datas,date
	with open("config/AH-structure.txt","r") as myfile:
		startID = myfile.readline().strip()
		f = startID
		startID = int(startID)
		date = datetime(year=int(f[0:4]),month=int(f[4:6]),day=int(f[6:8]),hour=int(f[8:10]),minute=int(f[10:12]),second=int(f[12:14]))
		datas={}
		for line in myfile:
			line = line.split("\t")
			datas[int(line[0])] = WowObject(item=line[1],owner=line[2],bid=line[3],bidChange=line[4],buyout=line[5],quantity=line[6],timeLeft=line[7],timeBegin=line[8],timeSell=line[9])
	with open("results/structure/general.txt","r") as myfile:
		n12 = int(myfile.readline())
		n24 = int(myfile.readline())
		n48 = int(myfile.readline())
		n2448 = int(myfile.readline())
		nNone = int(myfile.readline())
		bid = int(myfile.readline())
		buy = int(myfile.readline())
		notBuy = int(myfile.readline())
	with open("results/structure/items.json","r") as myfile:
		items = json.load(myfile)
	with open("results/structure/sellers.json","r") as myfile:
		sellers = json.load(myfile)

def save():
	global n12,n24,n48,n2448,nNone,bid,buy,notBuy,sellers,items,ID,datas
	with open("config/AH-structure.txt","w") as myfile:
		myfile.write(str(ID)+"\n")
		for key in datas:
			datas[key].save(key,myfile)
	with open("results/structure/general.txt","w") as myfile:
		myfile.write(str(n12)+"\n")
		myfile.write(str(n24)+"\n")
		myfile.write(str(n48)+"\n")
		myfile.write(str(n2448)+"\n")
		myfile.write(str(nNone)+"\n")
		myfile.write(str(bid)+"\n")
		myfile.write(str(buy)+"\n")
		myfile.write(str(notBuy)+"\n")
	with open("results/structure/items.json","w") as myfile:
		json.dump(items,myfile)
	with open("results/structure/sellers.json","w") as myfile:
		json.dump(sellers,myfile)

def main():
	global n12,n24,n48,n2448,nNone,bid,buy,notBuy,sellers,items,startID,datas,date,ID
	start = datetime(year=2015,month=11,day=1,hour=0,minute=0,second=0)
	# n12 = 0
	# n24 = 0
	# n48 = 0
	# n2448 = 0
	# nNone = 0
	# bid = 0
	# buy = 0
	# notBuy = 0

	# # sellers = defaultdict(lambda :defaultdict(lambda: defaultdict(lambda :0)))
	# # items = defaultdict(lambda: defaultdict(lambda :0))
	# sellers = {}
	# items = {}

	interBuy = defaultdict(lambda: interStat())
	interNotBuy = defaultdict(lambda: interStat())
	interSale = defaultdict(lambda: interStat())
	interUpToSale = defaultdict(lambda: interStat())

	path = "results/scanner"
	files = sorted(listdir(path))

	load()

	# f = files[0]
	# date = datetime(year=2015,month=11,day=1,hour=0,minute=0,second=0)
	# datas = {}
	for f in files:
		ID = f[:14]
		if int(ID) <= startID:
			continue
		preDate = date
		preDatas = datas
		date = datetime(year=int(f[0:4]),month=int(f[4:6]),day=int(f[6:8]),hour=int(f[8:10]),minute=int(f[10:12]),second=int(f[12:14]))
		inter = date-preDate
		inter = int(inter.total_seconds())
		if inter > 5000:
			inter = 0

		f = join(path,f)
		print(date)

		f = open(f,"r")
		data = json.load(f)
		datas={}
		for auction in data["auctions"]:
			if(auction["auc"] not in preDatas):
				datas[auction["auc"]] = WowObject(data = auction,time=date,inter=inter)
				obj = datas[auction["auc"]]
				sellers.setdefault(obj.owner, {}).setdefault(obj.item,{}).setdefault("QSale",0)
				items.setdefault(obj.item,{}).setdefault("QSale",0)
				sellers[obj.owner][obj.item]["QSale"] += obj.quantity
				items[obj.item]["QSale"] += obj.quantity

				if obj.timeBegin != None:
					interUpToSale[obj.item].add(obj.buyout,obj.bid,obj.quantity)
			else:
				datas[auction["auc"]] = preDatas[auction["auc"]].update(auction,date)
			obj = datas[auction["auc"]]
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
						sellers.setdefault(obj.owner, {}).setdefault(obj.item,{}).setdefault("QBuy",0)
						items.setdefault(obj.item,{}).setdefault("QBuy",0)
						sellers[obj.owner][obj.item]["QBuy"] += obj.quantity
						items[obj.item]["QBuy"] += obj.quantity

						interBuy[obj.item].add(obj.buyout,obj.bid,obj.quantity)
					elif res[0]:
						bid += 1
						sellers.setdefault(obj.owner, {}).setdefault(obj.item,{}).setdefault("QBuy",0)
						items.setdefault(obj.item,{}).setdefault("QBuy",0)
						sellers[obj.owner][obj.item]["QBuy"] += obj.quantity
						items[obj.item]["QBuy"] += obj.quantity

						interBuy[obj.item].add(obj.buyout,obj.bid,obj.quantity)
					else:
						notBuy += 1
						interNotBuy[obj.item].add(obj.buyout,obj.bid,obj.quantity)
		f.close()

		save()

		for key in interBuy:
			with open("results/structure/buy/"+str(key)+".txt", "a") as myfile:
				interBuy[key].save(ID, date, start, myfile)
		for key in interNotBuy:
			with open("results/structure/notbuy/"+str(key)+".txt", "a") as myfile:
				interNotBuy[key].save(ID, date, start, myfile)
		for key in interSale:
			with open("results/structure/sale/"+str(key)+".txt", "a") as myfile:
				interSale[key].save(ID, date, start, myfile)
		for key in interUpToSale:
			with open("results/structure/uptosale/"+str(key)+".txt", "a") as myfile:
				interUpToSale[key].save(ID, date, start, myfile)

if __name__ == '__main__':
	main()

