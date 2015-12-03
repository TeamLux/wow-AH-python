from datetime import *
import random

class WowObject:
	def __init__(self,data = None,time = None, inter = None,
		item= None,owner= None,bid= None,bidChange= None,buyout= None,quantity= None,timeLeft= None,timeBegin= None,timeSell= None):
		if data!=None and time != None and inter!= None:
			self.item = data["item"]
			self.owner = data["owner"]+"_"+data["ownerRealm"]
			self.bid = data["bid"]
			self.bidChange = False
			self.buyout = data["buyout"]
			self.quantity = data["quantity"]
			self.timeLeft = data["timeLeft"]
			if inter != 0:
				self.timeBegin = time
				self.timeSell = 12 if self.timeLeft == "LONG" else 2448
			else:
				self.timeBegin = None
				self.timeSell = None
		else:
			self.item = int(item)
			self.owner = owner
			self.bid = int(bid)
			self.bidChange = bidChange == "True"
			self.buyout = int(buyout)
			self.quantity = int(quantity)
			self.timeLeft = timeLeft
			if timeBegin == "None":
				self.timeBegin = None
				self.timeSell = None
			else :
				f = timeBegin
				self.timeBegin = datetime(year=int(f[0:4]),month=int(f[4:6]),day=int(f[6:8]),hour=int(f[8:10]),minute=int(f[10:12]),second=int(f[12:14]))
				self.timeSell = int(timeSell)

	def update(self,data,time):
		if data["item"]!=self.item and data["owner"]+"_"+data["ownerRealm"] != self.owner:
			print("BUG")
			return False
		if self.bid != data["bid"]:
			self.bid = data["bid"]
			self.bidChange = True
		if self.timeBegin != None and data["timeLeft"] == "LONG" and self.timeLeft == "VERY_LONG":
			if time - self.timeBegin > timedelta(days=1):
				self.timeSell = 48
			else:
				self.timeSell = 24
		self.timeLeft = data["timeLeft"]
		return self

	def isBuy(self,time,inter):
		if inter != 0:
			if self.timeLeft == "SHORT":
				return (False,self.buyout) if not self.bidChange else (True,self.bid)
			else:
				return (self.buyout)
		else:
			return None

	def save(self,ID,f):
		l = [str(ID),str(self.item),str(self.owner),str(self.bid),str(self.bidChange),str(self.buyout),str(self.quantity),str(self.timeLeft),str(self.timeBegin),str(self.timeSell)]
		f.write("\t".join(l)+"\n")