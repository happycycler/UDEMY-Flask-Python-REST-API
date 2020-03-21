from flask_restful import Resource, reqparse
from models.course import CourseModel
from datetime import datetime, timedelta
from platform import system

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
        'allrequests',
        type=str,
        required=False
    )

    postparser = reqparse.RequestParser()
    postparser.add_argument(
        'classname',
        type=str,
        required=True
    )
    postparser.add_argument(
        'startdate',
        type=str,
        required=True
    )
    postparser.add_argument(
        'enddate',
        type=str,
        required=True
    )
    postparser.add_argument(
        'starttime',
        type=str,
        required=True
    )
    postparser.add_argument(
        'endtime',
        type=str,
        required=True
    )
    postparser.add_argument(
        'orgid',
        type=int,
        required=True
    )
    postparser.add_argument(
        'userid',
        type=int,
        required=True
    )
    postparser.add_argument(
        'classdays',
        type=str,
        required=True
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
            courses = CourseModel.find_by_userid(data['userid'], data['allrequests'])
            if courses:
                return {'courses': [course.json() for course in courses]}
            return {'message': "No courses for userid '{}' were found.".format(data['userid'])}, 400
        else:
            return {'message': "Parameter 'id' or 'userid' is required."}, 400

    def post(self):
        data = Course.postparser.parse_args()

        classname = data['classname']
        startdate = datetime.strptime(data['startdate'], "%Y-%m-%d")
        enddate = datetime.strptime(data['enddate'], "%Y-%m-%d")
        # starttime = datetime.strptime(data['starttime'], "%I:%M %p") if system() == 'Windows' else datetime.strptime(data['starttime'], "%-I:%M %p")
        # endtime = datetime.strptime(data['endtime'], "%I:%M %p") if system() == 'Windows' else datetime.strptime(data['endtime'], "%-I:%M %p")
        starttime = datetime.strptime(data['starttime'], "%I:%M %p")
        endtime = datetime.strptime(data['endtime'], "%I:%M %p")
        orgid = data['orgid']
        userid = data['userid']
        if data['classdays'] == None:
            classdays = [datetime.weekday(startdate)]
        else:
            classdays = list(map(int, data['classdays'].split(',')))

        jsonstr = []
        msgstr = []
        for n in range(int (((enddate + timedelta(days=1)) - startdate).days)):
            classdate = startdate + timedelta(n)
            day = datetime.weekday(classdate)
            # print(datetime.strftime(classdate, "%Y-%m-%d") + ' - ' + str(day))
            if day in classdays:
                # print(classdate)
                # print(datetime.strftime(starttime, "%H:%M"))
                # print(datetime.strftime(endtime, "%H:%M"))
                course = CourseModel(orgid,
                                     classname,
                                     datetime.strftime(starttime, "%H:%M"),
                                     datetime.strftime(endtime, "%H:%M"),
                                     datetime.strftime(classdate, "%Y-%m-%d"),
                                     datetime.strftime(startdate, "%Y-%m-%d"),
                                     datetime.strftime(enddate, "%Y-%m-%d"),
                                     data['classdays'] if data['classdays'] != None else datetime.weekday(startdate),
                                     userid,
                                     None,
                                     None,
                                     None,
                                     None)
                try:
                    course.save_to_db()
                except:
                    msgstr.append({'status': "ERROR", "code": 500})
                jsonstr.append(course.json())

        msgstr.append({'status': "SUCCESS", "code": 200})
        # jsonstr.append({'status': "SUCCESS", "code": 200})
        return {'courses': jsonstr,'messages': msgstr}

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

            if data['type'] == "takeclass":
                course.acceptuserid = data['userid']
                course.acceptdate = datetime.today()
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