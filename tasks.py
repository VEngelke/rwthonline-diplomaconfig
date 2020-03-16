from app import celery
from app.backend import downloader,net
import pickle

@celery.task
def download_task(node_id):
	print("started download task for node "+str(node_id))
	session=pickle.load(open("session.p","rb"))
	print(session)
	file_=open("xtest.txt",'w')
	file_.write(str(node_id))
	file_.close()
	down=downloader.downloadCourse(node_id,session)
