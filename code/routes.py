import requests
from datetime import datetime, timedelta
from flask import jsonify, render_template, request, redirect, flash
from app import db, app
from models import Results, Tasks
from forms import WebsiteForm
from worker import count_words


'''@celery.task
def parse_website_text(_id):
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
        http_status_code = res.status_code if res.status_code is not None else 400
        result = Results(address=address, words_count=words_count, http_status_code=res.status_code)
        task = Tasks.query.get(_id)
        task.task_status = 'FINISHED'
        db.session.add(result)
        db.session.commit()'''


@app.route('/', methods=['POST', 'GET'])
@app.route('/add_website', methods=['POST', 'GET'])
def website():
    website_form = WebsiteForm()
    if request.method == 'POST':
        if website_form.validate_on_submit():
            address = request.form.get('address')
            task = Tasks(address=address, timestamp=datetime.now(), task_status='NOT_STARTED')
            db.session.add(task)
            db.session.commit()
            count_words.delay(task._id)
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html', form=website_form, error=error)
    return render_template('add.html', form=website_form)


@app.route('/results')
def get_results():
    results = Results.query.all()
    print(results)
    return render_template('results.html', results=results)
