import re




def getName(text):
	o=re.findall("(?<=pStpkName\" type=\"hidden\" value=\")[^\"]+",text)
	return o[0]

def getKnotenID(text):
	m=re.findall("(?<=wbSPO.wbShow\\?pOrgNr=14153&pStpKnotenNr=)[0-9]+",text)
	return m



def getRecordTable(text):                       #returns RecordConfigTable as (2d) List of booleans                            
	n=re.findall("(?<=td class=\" C\">)[JN]",text)
	b=list(map(lambda x:True if x=='J' else False,n))
	res=[]
	for i in range(5):
		res.append(b[i:i+6])
	return res 

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def getChildNodes(text):
	m=re.findall("(?<=wbSPO.cbSPOContent\\?pStpKnotenNr=)[0-9]+",text)
	return f7(list(map(int,m)))


def getCredits(text):
	m=re.findall("(?<=pStpkCredits\" type=\"hidden\" value=\")[^\"]+",text)
	if(len(m)>0):
		return float(m[0].replace(',','.'))
	else:
		return 0


def getSearchKnoten(text):
	m=re.findall("(?<=wbSPO.wbShow\\?pStpKnotenNr=)[0-9]+",text)
	print("this works")
	return list(map(int,m))

def getSearchNumberOfPages(text):
	m=re.findall("(?<=select> von )[0-9]+",text)
	if(len(m)>0):
		return int(m[0])
	else:
		return 1

def getSearchNames(text):
	o=re.findall("(?<=kt kt1 TextToolTip \" title=\")[^\"]+",text)
	return o

def getSearchTitles(text):
	o=re.findall("(?<=coTableGR1   \">\n<td colspan=\"4\" class=\" L\">)[^\<]+",text)
	return o



