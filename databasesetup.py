from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_login import UserMixin


Base = declarative_base()

class User(UserMixin,Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key =True)
	username = Column(String(250), nullable = False)
	email = Column(String(250), unique = True)
	password = Column(String(500), nullable = False)

class Task(Base):
	__tablename__ = 'task'
	id = Column(Integer, primary_key = True)
	name = Column(String(500), nullable = False)
	deadline = Column(Date, nullable = False)
	complete = Column(Boolean, default = False)
	user = relationship(User)
	user_id = Column(Integer, ForeignKey('user.id'))

	@property
	def serialize(self):
		return{
			'id': self.id,
			'name': self.name,
			'deadline': self.deadline,
			'user': self.user_id,
		}

engine = create_engine('sqlite:///taskman.db')

Base.metadata.create_all(engine)