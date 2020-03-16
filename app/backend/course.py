from datetime import datetime

class Course:

	filename=""


	def __init__(self,name,node):
		self.name=name
		self.rootNode=node
		self.lastModified=datetime.now()