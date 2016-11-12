from flask import Flask
from flask import jsonify
from flask import g
from flask import abort
from flask import request


from models import initialize
from models import Course
from models import DATABASE

app = Flask(__name__)
PORT = 8000
DEBUG = True

@app.before_request
def before_request():
	g.db = DATABASE
	g.db.connect()

@app.after_request
def after_request(request):
	g.db.close()
	return request

@app.errorhandler(404)
def not_found(error):
	return jsonify( generate_response(404, error = 'Resource not found') )

@app.errorhandler(400)
def bad_request(error):
	return jsonify( generate_response(400, error = 'Bad request') )

@app.errorhandler(422)
def unprocessable_entity(error):
	return jsonify( generate_response(422, error = 'Unprocessable Entity') )


@app.route('/codigo/api/v1.0/courses', methods=['GET'])
def get_courses():
	courses = Course.select()
	courses = [ course.to_json() for course in courses ]
	return jsonify( generate_response(data = courses) )

@app.route('/codigo/api/v1.0/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
	course = try_course(course_id)
	return jsonify( generate_response(data = course.to_json() ) )
	

@app.route('/codigo/api/v1.0/courses/', methods=['POST'])
def post_course():
	if not request.json:
		abort(400)
		
	title = request.json.get('title', '')
	description = request.json.get('description', '')

	course = Course.new(title, description)
	if course is None:
		abort(422)
	return jsonify( generate_response(data = course.to_json()))
	

@app.route('/codigo/api/v1.0/courses/<int:course_id>', methods=['PUT'])
def put_course(course_id):
	course = try_course(course_id)
	if not request.json:
		abort(400)

	#practicar
	course.title = request.json.get('title', course.title)
	course.description = request.json.get('description', course.description)

	if course.save():
		return jsonify(generate_response(data = course.to_json() ))
	else:
		abort(422)

@app.route('/codigo/api/v1.0/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
	course = try_course(course_id)
	if course.delete_instance():
		return jsonify( generate_response(data = {} ))
	else:
		abort(422)

def try_course(course_id):
	try:
		return Course.get(Course.id == course_id)
	except Course.DoesNotExist:
		abort(404)


def generate_response(status = 200, data = None, error = None):
	return {'status': status, 'data': data, 'error': error  }

if __name__ == '__main__':
	initialize()
	app.run(port = PORT, debug = DEBUG)
