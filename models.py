from peewee import *
import datetime

DATABASE = MySQLDatabase('REST', host='localhost', user='root', passwd='')

class Course(Model):
	class Meta:
		database = DATABASE
		db_table = 'courses'

	title = CharField(unique=True,max_length=250)
	description = TextField()
	created_at = DateTimeField(default= datetime.datetime.now() )

	def to_json(self):
		return {'id': self.id, 'title': self.title, 'description': self.description}

	@classmethod
	def new(cls, title, description):
		try:
			return cls.create(title = title, description = description)
		except IntegrityError:
			print("Error de integridad")
			return None

def create_course():
	title = 'Curso Flask'
	description = 'Curso gratuito de Flask'

	if not Course.select().where(Course.title == title):
		Course.create(title = title, description = description)

def initialize():
	DATABASE.connect()
	DATABASE.create_tables(  [Course], safe=True)
	create_course()
	DATABASE.close()

