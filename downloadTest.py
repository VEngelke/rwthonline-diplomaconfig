from app.backend import net
import os


def main():
	l=createList()
	n=net.Net()
	n.login('stmod','Rwth+123')

	for x in l:
		n.downloadPage(x)

	



def createList():
	l=[]
	for filename in os.listdir('cache'):
		s=os.path.splitext(filename)[0]
		if(s.isdigit()):
			l.append(int(s))
	return l


if __name__ == '__main__':
    main()