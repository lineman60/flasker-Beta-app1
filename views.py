__author__ = 'Beryl'
#views.py

from flask import Flask, flash, redirect, render_template, request, \
    session, url_for

from functools import wraps

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.exc import IntegrityError

from forms import AddTaskForm, RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from models import Task, User

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Errror in the %s field - %s" %(getattr(form, field).label.text, error), 'error')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for Registering. please log in')
            return redirect(url_for('login'))
        else:
            flash_errors(form)
            return render_template('registration.html', form=form, error=error)
    if request.method == 'GET':
        return render_template('registration.html', form=form)





def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out, C\'ya')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User.query.filter_by(
                name=request.form['name'],
                password=request.form['password']
            ).first()
            if u is None:
                error = 'Invalid username or password.'
                return render_template(
                    "login.html",
                    form=form,
                    error=error
                )
            else:
                session['logged_in'] = True
                session['user_id'] = u.id
                flash('You are logged in. Go Crazy.')
                return redirect(url_for('tasks'))
        else:
            return render_template(
                "login.html",
                form=form,
                error=error
            )
    if request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
    closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())
    return render_template('tasks.html', form=AddTaskForm(request.form), open_tasks=open_tasks, closed_tasks=closed_tasks)

#add new Tasks:
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
    import datetime
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(
                form.name.data,
                form.due_date.data,
                form.priority.data,
                datetime.datetime.utcnow(),
                '1',
                '1'
            )
            db.session.add(new_task)
            db.session.commit()
            flash('New entry was successfully posted. Thanks.')
    return redirect(url_for('tasks'))
# @login_required
# def new_task():
#     import datetime
#     error = None
#     form = AddTaskForm(request.form)
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             new_task = Task(
#                 form.name.data,
#                 form.due_date.data,
#                 form.priority.data,
#                 '1')
#             db.session.add(new_task)
#             db.session.commit()
#             flash('new entery was successfully posted. Thanks')
#             print(new_task)
#             return redirect(url_for('tasks'))
#         else:
#             print('else')
#             return redirect(url_for('tasks'))

# Mark tasks as complete:
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({"status": "0"})
    db.session.commit()
    flash('the task was marked as complete. ')
    return redirect(url_for('tasks'))

#delete Tasks:


@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('the task was deleted.')
    return redirect(url_for('tasks'))