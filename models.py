from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, EqualTo
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import date
from flask_login import AnonymousUserMixin

class registerForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired(),InputRequired(message= " No Data Was Provided")])
	email = StringField('Email', validators = [DataRequired(),InputRequired(message= " No Data Was Provided")])
	password = PasswordField('Password', validators = [DataRequired(),InputRequired(message= " No Data Was Provided"),EqualTo('confirm', message = 'Password Must Match')])
	confirm = PasswordField('Repeat password')

class loginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(),InputRequired(message= " No Data Was Provided")])
	password_login = PasswordField('Password', validators = [DataRequired(),InputRequired(message= " No Data Was Provided")])

class createTaskForm(FlaskForm):
	task_name = StringField('Task Name', validators = [DataRequired(),InputRequired(message= "No Data Was Provided")])
	task_date = DateField('Task Deadline Date', format = '%Y-%m-%d', validators = [DateRange(min=date.today())])

class myAnonymous(AnonymousUserMixin):
	def __init__(self):
		self.username = 'Guest'
		self.id = 'None'

	def get_id(self):
		return None