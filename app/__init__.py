from flask import Flask
from config import Config
from celery import Celery
import os

downloadedCourses=[]
session=None
lastEdit=None
app = Flask(__name__)
app.debug =True
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config.from_object(Config)





broker_url = os.getenv('CELERY_BROKER_URL', 'filesystem://')
broker_dir = os.getenv('CELERY_BROKER_FOLDER', './broker')

for f in ['out', 'processed']:
    if not os.path.exists(os.path.join(broker_dir, f)):
        os.makedirs(os.path.join(broker_dir, f))


celery = Celery(__name__)
celery.conf.update({
    'broker_url': broker_url,
    'broker_transport_options': {
        'data_folder_in': os.path.join(broker_dir, 'out'),
        'data_folder_out': os.path.join(broker_dir, 'out'),
        'data_folder_processed': os.path.join(broker_dir, 'processed')
    },
    'imports': ('tasks',),
    'result_persistent': True,
    'results_backend':os.path.join(broker_dir, 'results'),
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']})

from app import routes
