from flask_restful import Resource, reqparse
from models.course import CourseModel
from datetime import datetime

class Course(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'id',
        type=int,
        required=False
    )
    getparser.add_argument(
        'userid',
        type=int,
        required=False
    )
    getparser.add_argument(
        'subrequests',
        type=str,
        required=False
    )

    putparser = reqparse.RequestParser()
    putparser.add_argument(
        'id',
        type=int,
        required=False
    )
    putparser.add_argument(
        'userid',
        type=int,
        required=False
    )
    putparser.add_argument(
        'type',
        type=str,
        required=False
    )

    def get(self):
        data = Course.getparser.parse_args()
        if data['id'] is not None:
            course = CourseModel.find_by_id(data['id'])
            if course:
                return course.json()
            return {'message': "A course with id '{}' was not found.".format(data['id'])}, 400
        elif data['userid'] is not None:
            courses = CourseModel.find_by_userid(data['userid'], data['subrequests'])
            if courses:
                return {'courses': [course.json() for course in courses]}
            return {'message': "No courses for userid '{}' were found.".format(data['userid'])}, 400
        else:
            return {'message': "Parameter 'id' or 'userid' is required."}, 400

    def post(self, id):
        data = Course.putparser.parse_args()
        course = CourseModel.find_by_id(data['id'])

        course = CourseModel(name)
        try:
            course.save_to_db()
        except:
            return {'message': "An error occurred inserting the course."}, 500

        return course.json(), 201

    def delete(self, name):
        course = CourseModel.find_by_name(name)
        if course:
            course.delete_from_db()
            return {'message': 'Course deleted successfully.'}
        return {'message': "A course with the name '{}' was not found.".format(name)}, 400

    def put(self):
        data = Course.putparser.parse_args()
        course = CourseModel.find_by_id(data['id'])

        if course:
            if data['type'] == "confirmrequest":
                course.requestuserid = data['userid']
                course.requestdate = datetime.today()
                course.save_to_db()

            if data['type'] == "cancelrequest":
                course.requestuserid = None
                course.requestdate = None
                course.save_to_db()

            if data['type'] == "canceltake":
                course.acceptuserid = None
                course.acceptdate = None
                course.save_to_db()

        else:
            return {'message': "A course with the id '{}' was not found.".format(data['id'])}, 400

            course.save_to_db()
        return course.json()

class CourseList(Resource):
    def get(self):
        # return {'courses': [course.json() for course in CourseModel.query.all()]}
        return {'courses': [course.json() for course in CourseModel.query.filter(CourseModel.classdate >= datetime.today()).order_by(CourseModel.classdate,CourseModel.starttime,CourseModel.name).all()]}