import os

import requests
from celery import Celery
from models import Results, Tasks
from app import db

TIMEOUT = 10
EXPIRES = 300

app = Celery('count', broker=os.getenv('CELERY_BROKER_URL'), backend=os.getenv('CELERY_RESULT_BACKEND'))

app.conf.update(
    result_expires=EXPIRES,
)


@app.task
def count_words(_id):
    task = Tasks.query.get(_id)
    task.task_status = 'PENDING'
    db.session.commit()
    address = task.address
    if not (address.startswith('http') and address.startswith('https')):
        address = 'http://' + address
    with app.app_context():
        res = requests.get(address)
        words_count = 0
        if res.ok:
            words = res.text.split()
            words_count = words.count("Python")
        #http_status_code = res.status_code if res.status_code is not None else 400
        result = Results(address=address, words_count=words_count, http_status_code=res.status_code)
        task = Tasks.query.get(_id)
        task.task_status = 'FINISHED'
        db.session.add(result)
        db.session.commit()