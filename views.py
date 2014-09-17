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
    return render_template('tasks.html', form=AddTaskForm(request.form), open_task=open_task,
     closed_tasks=closed_tasks
    )

#add new Tasks:
@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    g.db = connect_db()
    name = request.form['name']
    date= request.form['due_date']
    priority = request.form['priority']
    if not name or not date or not priority:
        flash("All fields are required. Please try again")
        return redirect(url_for('tasks'))
    else:
        g.db.execute('insert into tasks (name, due_date, priority, status) values (?, ?, ?, 1)', [request.form['name'], request.form['due_date'],
                     request.form['name'], request.form['due_date'], request.form['priority']])
        g.db.commit()
        g.db.close()
        flash('new entery was successfully posted. Thanks')
        return redirect(url_for('tasks'))

# Mark tasks as complete:
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    g.db = connect_db()
    g.db.execute(
        'update tasks set status = 0 where task_id='+str(task_id)
    )
    g.db.commit()
    g.db.close()
    flash('the task was marked as complete. ')
    return redirect(url_for('tasks'))

#delete Tasks:
@pp.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute('delete from tasks where task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('the task was deleted.')
    return redirect(url_for('tasks'))