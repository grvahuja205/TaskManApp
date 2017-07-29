from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasesetup import User, Task, Base
from passlib.hash import sha256_crypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import date, timedelta
from models import registerForm, loginForm, createTaskForm, myAnonymous
import json
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

app.secret_key = 'super_secret_key'

engine = create_engine('sqlite:///taskman.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(hours = 8)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = myAnonymous

csrf = CSRFProtect()
csrf.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id = int(user_id)).one()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
	lform = loginForm(request.form)
	if request.method == 'POST' and lform.validate():
		email = request.form['email']
		print type(email)
		password = request.form['password_login']
		auser = session.query(User).filter_by(email = email).one()
		if auser:
			if sha256_crypt.verify(password, auser.password):
				login_user(auser)
				return redirect(url_for('dashboard', user_id = auser.id))
			else:
				flash("Bad Password")
				return redirect(url_for('login'))
		else:
			flash("Kindly register yourself first")
			return render_template('register.html')
	else:
		return render_template('login.html', form = lform)

@app.route('/register/', methods = ['GET', 'POST'])
def register():
	rform = registerForm(request.form)
	if request.method == 'POST' and rform.validate():
		print "inside form"
		uname = request.form['username']
		email = request.form['email']
		print type(email)
		password = sha256_crypt.encrypt(str(request.form['password']))
		ruser = session.query(User).filter_by(email = email).count()
		if ruser != 0:
			us = session.query(User).filter_by(email = email).one()
			print "user already there with email %s" %us.email
			flash('User Already Registered With This Email ID')
			return redirect(url_for('register'))
		else:
			print "creating user"
			newUser = User(username = uname, email = email, password = password)
			session.add(newUser)
			session.commit()
			created_user = session.query(User).filter_by(email = email).one()
			flash("User User ID Created With Username As Your Email")
			return redirect(url_for('dashboard', user_id = created_user.id))
	else:
		return render_template('register.html', form = rform)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("User logged out successfully")
	return redirect(url_for('index'))

@app.route('/dashboard/<int:user_id>/', methods = ['GET', 'POST'])
@login_required
def dashboard(user_id):
	if user_id != current_user.id:
		flash("Wrong User")
		return redirect(url_for('login'))
	tasks = session.query(Task).filter_by(user_id = user_id).all()
	auser = session.query(User).filter_by(id = user_id).one()
	return render_template('dashboard.html', tasks = tasks, id = auser.id)

@app.route('/createtask/<int:user_id>/', methods = ['GET', 'POST'])
@login_required
def createTask(user_id):
	cform = createTaskForm(request.form)
	if user_id != current_user.id:
		flash("Wrong User")
		return redirect(url_for('login'))
	if request.method == 'POST' and cform.validate():
		tname = request.form['task_name']
		tdate = request.form['task_date']
		sdate = tdate.split('-')
		adate = date(int(sdate[0]), int(sdate[1]), int(sdate[2]))
		if_t = session.query(Task).filter_by(name = tname).count()
		if if_t > 0:
			flash("This task is already created")
		else:
			newTask = Task(name = tname, deadline = adate, user_id = current_user.id)
			session.add(newTask)
			session.commit()
		return redirect(url_for('dashboard', user_id = current_user.id))
	else:
		return render_template('createtask.html', form = cform)

@app.route('/marktask/<int:task_id>/', methods = ['GET', 'POST'])
@login_required
def markTask(task_id):
	task = session.query(Task).filter_by(id = task_id).one()
	if task.user_id != current_user.id:
		flash("Wrong User")
		return redirect(url_for('login'))
	if request.method == 'POST':
		if task.complete == True:
			task.complete = 0
			session.add(task)
			session.commit()
			return redirect(url_for('dashboard', user_id = current_user.id))
		else:
			task.complete = True
			session.add(task)
			session.commit()
			return redirect(url_for('dashboard', user_id = current_user.id))
	else:
		return render_template('marktask.html', task = task)

@app.route('/deletetask/<int:task_id>/', methods = ['GET', 'POST'])
@login_required
def deleteTask(task_id, methods = ['GET', 'POST']):
	task = session.query(Task).filter_by(id = task_id).one()
	if task.user_id != current_user.id:
		flash("Wrong User")
		return redirect(url_for('login'))
	if user_id != current_user.id:
		flash("Wrong User")
		return redirect(url_for('login'))
	if request.method == 'POST':
		session.delete(task)
		session.commit()
		return redirect(url_for('dashboard', user_id = current_user.id))
	else:
		return render_template('deletetask.html', task = task)

@app.route('/tasks', methods = ['GET', 'POST'])
def taskJSON():
	tasks = session.query(Task).all()
	if request.method == 'POST':
		data = json.loads(request.data)
		tname =  data.get("task_name")
		tdate = data.get("task_deadline")
		sdate = tdate.split('-')
		adate = date(int(sdate[0]), int(sdate[1]), int(sdate[2]))
		if_t = session.query(Task).filter_by(name = tname).count()
		if if_t > 0:
			response = make_response(json.dumps('Task Already Exists.'), 401)
		else:
			newTask = Task(name = tname, deadline = adate, user_id = current_user.id)
			session.add(newTask)
			session.commit()
			response = make_response(json.dumps('Task Created.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		return jsonify(Tasks=[i.serialize for i in tasks])

@app.route('/tasks/<int:task_id>', methods= ['DELETE'])
def taskDeleteJSON(task_id):
	task_c = session.query(Task).filter_by(id = task_id).count()
	if task_c > 0:
		task = session.query(Task).filter_by(id = task_id).one()
		if request.method == 'DELETE' and task.user_id == None:
			session.delete(task)
			session.commit()
			response = make_response(json.dumps('Task Deleted'), 200)
		else:
			response = make_response(json.dumps('Wrong Method Used or Trying To Delete Protected Task'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
	else:
		response = make_response(json.dumps('No Such Task Exixts'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def page_not_found(e):
    return render_template('404.html'), 401

@app.errorhandler(NoResultFound)
def handle_NoResult_Error(e):
    return render_template('NoResutl.html')

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 7000)