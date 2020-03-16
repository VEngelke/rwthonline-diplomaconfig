from app.backend import net,node,course
from app.backend import regex 
import os
import re
import pickle


global sess

def downloadCourse(rootId,session):
	global sess
	sess=session
	sess.downloadPage(rootId)

	root=node.Node(rootId)

	buildTree(root)


	c=course.Course(root.name,root)
	pickle.dump(c,open("storage/"+c.name+"_"+str(c.lastModified)+".p","wb"),protocol=2)


	



def buildTree(currentNode):
	print(currentNode.id)
	d=loadData(currentNode.id)
	#print(d)
	modifyNode(currentNode,d)
	for n in currentNode.childNodes:
		buildTree(n)


def modifyNode(currentNode,data):
	currentNode.recordTable=getRecordTable(data)
	currentNode.name=getName(data)
	currentNode.credits=regex.getCredits(data)
	childs=getChildNodes(data)
	page=2
	b=re.findall("pPageNr="+str(page),data)

	while(len(b)>0):


		moredata=getMorePages(currentNode.id,page)
		childs=childs+getChildNodes(moredata)
		page=page+1
		b=re.findall("pPageNr="+str(page),data)

	for i in childs:
		currentNode.childNodes.append(node.Node(i))


def loadData(id):
	global sess
	if os.path.exists(getFilePath(id)):
		return loadFile(getFilePath(id))
	else:
		sess.downloadPage(id)
	print("downloaded node "+str(id))
	return loadFile(getFilePath(id))
		


def loadFile(path):
	file=open(path)
	return file.read()

def getFilePath(id):
	return "cache/"+str(id)+".txt"


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def getChildNodes(text):
	m=re.findall("(?<=wbSPO.cbSPOContent\\?pStpKnotenNr=)[0-9]+",text)
	return f7(list(map(int,m)))

def getRecordTable(text):                       #returns RecordConfigTable as (2d) List of booleans                            
	n=re.findall("(?<=td class=\" C\">)[JN]",text)
	b=list(map(lambda x:True if x=='J' else False,n))
	res=[]
	for i in range(5):
		res.append(b[i:i+6])
	return res 

def getMorePages(id,page):
	global sess
	path=getMoreFilePath(id,page)

	if os.path.exists(path):
		return loadFile(path)
	else:
		sess.downloadFurtherPages(id,page)
	print("downloaded further pages for node "+str(id))
	return loadFile(path)

def getMoreFilePath(id,pagenr):
	return "cache/"+str(id)+'p'+str(pagenr)+".txt"

def getName(text):
	o=re.findall("(?<=pStpkName\" type=\"hidden\" value=\")[^\"]+",text)
	return o[0]


