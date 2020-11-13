import requests
from datetime import datetime, timedelta
from flask import jsonify, render_template, request, redirect, flash
from app import db, app
from models import Results, Tasks
from forms import WebsiteForm
from worker import count_words


@app.route('/', methods=['POST', 'GET'])
@app.route('/task', methods=['POST', 'GET'])
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
    return render_template('results.html', results=results)
