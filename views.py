__author__ = 'Beryl'
#views.py

from flask import Flask, flash, redirect, render_template, request, \
    sessions, url_for, g

from functools import wraps

import sqlite3

app = Flask(__name__)
app.config.from_object('config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in sessions:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    sessions.pop('logged_in', None)
    flash('You are logged out, C\'ya')
    return redirect(url_for('login'))

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
            or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentinals. Plase try again'
            return render_template('login.html', error=error)
        else:
            sessions['logged_in'] = True
            return redirect(url_for('tasks'))
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/tasks')
@login_required
def task():
    g.db = connect_db()
    cur = g.db.execute(
        'select name, due_date, priority, task_id, from tasks where status=1'
    )
    open_task = [dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('tasks.html', form=AddTaslForm(request.form), open_task=open_task,
     closed_tasks=closed_tasks
    )