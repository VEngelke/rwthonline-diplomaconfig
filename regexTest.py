import re
import os


def main():
	file=open("search/chemie.txt")
	text=file.read()
	x=text.split('coTableGR1')
	for s in x:
		print(getSearchKnoten(s))
	print(getSearchTitles(text))





def getSearchKnoten(text):
	m=re.findall("(?<=wbSPO.wbShow\\?pStpKnotenNr=)[0-9]+",text)
	print("this works")
	return list(map(int,m))


def getSearchTitles(text):
	o=re.findall("(?<=coTableGR1   \">\n<td colspan=\"4\" class=\" L\">)[^\<]+",text)
	return o


if __name__ == '__main__':
    main() 