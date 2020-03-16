class Node:
	id=-1
	name=""
	credits

	def __init__(self,id,name="default"):
		self.id=id
		self.name=name
		self.childNodes=[]
		self.recordTable=[]





def printTree(node,depth):
	printNode(node,depth)
	for n in node.childNodes:
		printTree(n,depth+1)

def printNode(node,depth):
	#print(" "*depth)
	print(" "*depth*2+str(node.id)+" "+str(node.name))



def main():
	test = Node(100,"Informatik")
	#test.n=42
	#print(test,n)
	t1=Node(101,"Praktische Informatik")
	t3=Node(1011,"Programmierung")
	t1.childNodes.append(t3)
	t2=Node(102,"Theoretische Informatik")
	test.childNodes.append(t1)
	test.childNodes.append(t2)
	print(test.childNodes)
	printTree(test,0)

	#print(test.child_nodes[0].name)

	for n in test.childNodes:
		print(n.name)



if __name__ == '__main__':
    main()