import requests
import xml.etree.ElementTree as ET
import urllib
import json


class Net:
	



	def __init__(self):
		self.session=requests.Session()


	def login(self,username,password):

		response=self.session.post('https://qs-online.rwth-aachen.de/RWTHonline/ee/rest/auth/user')
		xml=ET.fromstring(response.text);
		authUrl=xml[0][0][0][0].text
		authUrl=authUrl.replace("{username}",urllib.parse.quote(username))
		authUrl=authUrl.replace("{password}",urllib.parse.quote(password))


		#print(authUrl)
		response=self.session.post(authUrl)
		#printResponse(response)
		#j=json.loads(response.text)
		#auth="Bearer "+j["access_token"]
		#print(auth)

		res=self.session.get('https://qs-online.rwth-aachen.de/RWTHonline/pl/ui/$ctx;lang=de/wbSPO.cbSPOContent?pStpKnotenNr=3197&pORgNr=14153')
				
		#printResponse(res)
		#if(res.status_code==200):
		if(int(res.headers['content-length'])>10000):
			return True
		else:
			return False


	def downloadPage(self,id):
		res=self.session.get('https://qs-online.rwth-aachen.de/RWTHonline/pl/ui/$ctx;lang=de/wbSPO.cbSPOContent/?pStpKnotenNr='+str(id)+'&pORgNr=14153')
		page=res.text
		file_=open("cache/"+str(id)+".txt",'w')
		file_.write(page)
		file_.close()

	def downloadFurtherPages(self,id,pagenr):
		res=self.session.get('https://qs-online.rwth-aachen.de/RWTHonline/pl/ui/$ctx;lang=de/wbSPO.cbSPOChildElements?pStpKnotenNr='+str(id)+'&pOrgNr=14153&pPageNr='+str(pagenr))
		page=res.text
		file_=open("cache/"+str(id)+'p'+str(pagenr)+".txt",'w')
		file_.write(page)
		file_.close()


	def getSearchResult(self,search,page=1):
		res=self.session.get('https://qs-online.rwth-aachen.de/RWTHonline/pl/ui/$ctx;lang=de/wbSPOMeta.wbSPOs/NC_1931?pOrgNr=14153&pSort=&pFilter=null%3Ff_4_10%3D'+search+'&pPageNr='+str(page))
		page=res.text
		file_=open("search/"+search+".txt",'w')
		file_.write(page)
		file_.close()
		return page







	def checkConnection(self):
		print("checking connection")
		res=self.session.get('https://qs-online.rwth-aachen.de/')




def printResponse(res):
	print(res.status_code)
	print(res.headers)
	print(res.text)