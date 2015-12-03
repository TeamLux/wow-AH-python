import urllib.request
import json
import datetime
import time

class Scanner(object):
	def __init__(self, realm, locale, api_key, lastModified=0):
		self.realm = realm
		self.locale = locale
		self.api_key = api_key
		self.lastModified = lastModified

	def scan(self):
		f = urllib.request.urlopen("https://eu.api.battle.net/wow/auction/data/"+self.realm+"?locale="+self.locale+"&apikey="+self.api_key)
		s = f.read().decode(encoding='UTF-8')
		json_res = json.loads(s)
		datas = urllib.request.urlopen(json_res["files"][0]["url"])
		modif = json_res["files"][0]["lastModified"]
		if modif != self.lastModified:
			f = open("results/scanner/"+str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))+".json","w")
			f.write(datas.read().decode(encoding='UTF-8'))
			f.close()
			open("config/AH-scanner.txt","w").write(str(modif))

def main():
	while True:
		try:
			lastModified = int(open("config/AH-scanner.txt").read().strip())
			scan = Scanner("garona","fr_FR","pjwwk5ex8gwtekdfyftes7wwy5bcuzmh", lastModified)
			scan.scan()
		except Exception as e:
			print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"error")
		time.sleep(60)

if __name__ == '__main__':
	main()