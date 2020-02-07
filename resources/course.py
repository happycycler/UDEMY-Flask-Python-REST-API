from flask_restful import Resource, reqparse
from models.course import CourseModel

class Course(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument(
        'id',
        type=int,
        required=False,
        help='Store ID is required.'
    )
    getparser.add_argument(
        'userid',
        type=int,
        required=False,
        help='Store ID is required.'
    )

    def get(self):
        data = Course.getparser.parse_args()
        if data['id'] is not None:
            course = CourseModel.find_by_id(data['id'])
            if course:
                return course.json()
            return {'message': "A course with id '{}' was not found.".format(data['id'])}, 400
        elif data['userid'] is not None:
            courses = CourseModel.find_by_userid(data['userid'])
            # return {'course': [course.json() for course in cls.query.filter_by(userid=userid)]}
            if courses:
                return {'course': [course.json() for course in courses]}
            return {'message': "No courses for userid '{}' were found.".format(data['userid'])}, 400
        else:
            return {'message': "Parameter 'id' or 'userid' is required."}, 400



    # def get(self, userid):
    #     course = CourseModel.find_by_userid(userid)
    #     if course:
    #         return course.json()
    #     return {'message': "A course with the name '{}' was not found.".format(userid)}, 400

    def post(self, name):
        course = CourseModel.find_by_name(name)
        if course:
            return {'message': "A course with the name '{}' already exists.".format(name)}, 400

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

    def put(self, name):
        data = Course.parser.parse_args()

        course = CourseModel.find_by_name(name)

        if course is None:
            course = CourseModel(name)
        else:
            # course.name = data['name']
            return {'message': "A course with the name '{}' was not found.".format(data['name'])}, 400

            course.save_to_db()
        return course.json()

class CourseList(Resource):
    def get(self):
        return {'course': [course.json() for course in CourseModel.query.all()]}