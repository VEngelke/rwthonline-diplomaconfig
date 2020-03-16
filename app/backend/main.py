import node
import re
import driver
import os
import pickle

offline=False

def main():
	driver.init()
	#driver.downloadPage(d,107441)
	a=node.Node(3197)
	#r=getData(1)
	#print(r)
	#print (getChildNodes(r))
	#t=getRecordTable(r)
	#print(t)
	#buildTree(a)
	#node.printTree(a,0)
	#for i in a.childNodes:
	#	print (i.id)
	#print(a.recordTable)
	#print(getChildNodes(loadData(107136)))

	#pickle.dump(a,open("pickle/informatik.p","wb"))





	while (True):
		sid=input("Enter ID: ")
		print("Searching for "+str(sid))
		n=searchNode(int(sid),a)
		if n is None:
			print("no node found for id: "+sid)
		else:
			print("ID: "+str(n.id)+" Name:"+n.name)





def buildTree(currentNode):
	print(currentNode.id)
	d=loadData(currentNode.id)
	#print(d)
	modifyNode(currentNode,d)
	for n in currentNode.childNodes:
		buildTree(n)

def buildTreeDepth(currentNode,depth):
	print(currentNode.id)
	d=loadData(currentNode.id)
	#print(d)
	modifyNode(currentNode,d)
	if(depth>0):
		for n in currentNode.childNodes:
			buildTreeDepth(n,depth-1)


def modifyNode(currentNode,data):
	currentNode.recordTable=getRecordTable(data)
	currentNode.name=getName(data)
	childs=getChildNodes(data)
	page=2
	b=re.findall("pPageNr="+str(page),data)

	while(len(b)>0):


		moredata=getMorePages(currentNode.id,page)
		childs=childs+getChildNodes(moredata)
		page=page+1
		b=re.findall("pPageNr="+str(page),data)



	#print(childs)
	#print(getName(data))
	for i in childs:
		currentNode.childNodes.append(node.Node(i))



def loadData(id):
	if(offline):
		return loadFile(id)
	else:
		if os.path.exists(getFilePath(id)):
			return loadFile(getFilePath(id))
		else:
			driver.downloadPage(id)
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
	path=getMoreFilePath(id,page)
	if(offline):
		return loadFile(path)
	else:
		if os.path.exists(path):
			return loadFile(path)
		else:
			driver.downloadFurtherPages(id,page)
		print("downloaded further pages for node "+str(id))
		return loadFile(path)

def getMoreFilePath(id,pagenr):
	return "cache/"+str(id)+'p'+str(pagenr)+".txt"

def getName(text):
	o=re.findall("(?<=pStpkName\" type=\"hidden\" value=\")[^\"]+",text)
	return o[0]



def searchNode(id,currentNode):

	#print("Searching in "+str(currentNode.id))
	if(id==currentNode.id):
		print(type(currentNode))
		return currentNode
	else:
		for c in currentNode.childNodes:
			r=searchNode(id,c)
			if(r!=None):
				return r
		return None
		

def searchNodePath(id,currentNode):
	
	if(id==currentNode.id):
		print(type(currentNode))
		return (currentNode,[currentNode.id])
	else:
		for c in currentNode.childNodes:
			r,l=searchNodePath(id,c)
			if(r!=None):
				print(r.name)
				print("l is" +str(l))
				return (r,l.append(currentNode.id))
		print("nothing found")
		return (None,[1])


def s(id,currentNode):
	if(id==currentNode.id):
		return currentNode,[(currentNode.id,currentNode.name)]
	else:
		r=None
		l=None
		for c in currentNode.childNodes:
			rs,ls=s(id,c)
			if(rs!=None):
				r=rs
				l=ls+[(currentNode.id,currentNode.name)]
		return r,l



def filterNodes(currentNode,nlist):
	currentNode.childNodes=[x for x in currentNode.childNodes if x.id in nlist]
	for n in currentNode.childNodes:
		filterNodes(n,nlist)




if __name__ == '__main__':
    main()