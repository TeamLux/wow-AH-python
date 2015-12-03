import math

class interStat:
	def __init__(self):
		self.prices = []
		self.bidPrice = []
		self.total = 0
		self.bidTotal = 0
		self.n = 0

	def add(self,price,bid, q):
		self.prices.append((price,q))
		self.bidPrice.append((bid,q))
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
		return math.sqrt(som/n)

	def bidStd(self):
		mu = self.bidAvg()
		som = 0
		for p,q in self.bidPrices:
			som += q*((p-mu)**2)
		return math.sqrt(som/n)

	def save(self):
		self.prices = []
		self.bidPrice = []
		self.total = 0
		self.bidTotal = 0
		self.n = 0

