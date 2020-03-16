from selenium import webdriver





class Driver:
	def __init__(self):
		self.driver=webdriver.Chrome('/usr/bin/chromedriver')


	def openPage(self,url):
		
		self.driver.get('https://qs-online.rwth-aachen.de/RWTHonline/ee/ui/ca2/app/desktop/#/login?$ctx=rbacId=')

	def downloadPage(self,id):
		
		self.driver.get('https://qs-online.rwth-aachen.de/RWTHonline/pl/ui/$ctx;lang=de/wbSPO.cbSPOContent/?pStpKnotenNr='+str(id)+'&pORgNr=14154');
		page=self.driver.page_source
		file_=open("cache/"+str(id)+".txt",'w')
		file_.write(page)
		file_.close()

	def downloadFurtherPages(self,id,pagenr):
		self.driver.get('https://qs-online.rwth-aachen.de/RWTHonline/pl/ui/$ctx;lang=de/wbSPO.cbSPOChildElements?pStpKnotenNr='+str(id)+'&pOrgNr=14153&pPageNr='+str(pagenr))
		page=self.driver.page_source
		file_=open("cache/"+str(id)+'p'+str(pagenr)+".txt",'w')
		file_.write(page)
		file_.close()