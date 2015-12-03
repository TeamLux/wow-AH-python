import math
from operator import itemgetter

class interStat:
	def __init__(self):
		self.prices = []
		self.bidPrices = []
		self.total = 0
		self.bidTotal = 0
		self.n = 0

	def add(self,price,bid, q):
		self.prices.append((price,q))
		self.bidPrices.append((bid,q))
		self.total += price*q
		self.bidTotal += bid*q
		self.n += q

	def avg(self):
		return self.total/self.n

	def bidAvg(self):
		return self.bidTotal/self.n

	def std(self):
		mu = self.avg()
		som = 0
		for p,q in self.prices:
			som += q*((p-mu)**2)
		return math.sqrt(som/self.n)

	def bidStd(self):
		mu = self.bidAvg()
		som = 0
		for p,q in self.bidPrices:
			som += q*((p-mu)**2)
		return math.sqrt(som/self.n)

	def save(self,ID,time,start,f):
		avg = "None" if not self.n else str(self.avg())
		std = "None" if not self.n else str(self.std())
		avgb = "None" if not self.n else str(self.bidAvg())
		stdb = "None" if not self.n else str(self.bidStd())
		maxp = "None" if not self.prices else str(max(self.prices,key=itemgetter(0))[0])
		minp = "None" if not self.prices else str(min(self.prices,key=itemgetter(0))[0])
		maxb = "None" if not self.bidPrices else str(max(self.bidPrices,key=itemgetter(0))[0])
		minb = "None" if not self.bidPrices else str(min(self.bidPrices,key=itemgetter(0))[0])
		l = [str(ID),str(int((time-start).total_seconds())),str(self.n),maxp,minp,avg,std,maxb,minb,avgb,stdb]
		f.write("\t".join(l)+"\n")
		self.prices = []
		self.bidPrices = []
		self.total = 0
		self.bidTotal = 0
		self.n = 0

