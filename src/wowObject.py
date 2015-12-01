from datetime import *
import random

class WowObject:
	def __init__(self,data,time, inter):
		self.item = data["item"]
		self.owner = data["owner"]+"_"+data["ownerRealm"]
		self.bid = data["bid"]
		self.bidChange = False
		self.buyout = data["buyout"]
		self.quantity = data["quantity"]
		self.timeLeft = data["timeLeft"]
		if inter != 0:
			self.timeBegin = time-timedelta(seconds=random.randint(0,inter))
			self.timeSell = 12 if self.timeLeft == "LONG" else None
		else:
			self.timeBegin = None
			self.timeSell = None

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
		t = time-timedelta(seconds=random.randint(0,inter))
		if self.timeLeft == "SHORT":
			return (False,self.buyout,t) if not self.bidChange else (True,self.bid,t)
		else:
			return (self.buyout,t)