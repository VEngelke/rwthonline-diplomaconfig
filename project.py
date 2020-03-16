from app import app
from app.backend import node,course
from app import downloadedCourses
import pickle
import sys


import os

@app.before_first_request
def loadFiles():


	sys.path.append('app/backend')



	global downloadedCourses
	
	for filename in os.listdir('storage'):
		c=pickle.load(open("storage/"+filename,"rb"))
		c.filename=filename

		already_loaded=False

		for co in downloadedCourses:
			if co.filename==filename:
				already_loaded=True
		if (not already_loaded):		
			downloadedCourses.append(c)


	

	





