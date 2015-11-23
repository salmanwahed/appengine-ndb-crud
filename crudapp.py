# -*- coding: utf-8 -*-

import os
import urllib

import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from models import Student

DEFAULT_ROOT = 'default_student'

JINJA_ENV = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True
        )

def get_key(student_root=DEFAULT_ROOT):
    return ndb.Key('Student', student_root)

class MainPage(webapp2.RequestHandler):
    def get(self):
        student_root = self.request.get('student_root', DEFAULT_ROOT)
        student_query = Student.query(ancestor=get_key(student_root)).order(-Student.date)
        students = student_query.fetch()
        for st in students:
            print st.key
            print st.student_id

        template_values = {
                "students": students
                }
        template = JINJA_ENV.get_template('index.html')
        self.response.write(template.render(template_values))


class AddStudent(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('new_student.html')
        self.response.write(template.render())

    def post(self):
        student_root = self.request.get('student_root', DEFAULT_ROOT)
        student = Student(parent=get_key(student_root))
        student.name = self.request.get('name')
        student.registration = self.request.get('registration')
        student.department = self.request.get('department')
        student.email = self.request.get('email')
        skey = student.put()
        return webapp2.redirect('/')


class OneStudent(webapp2.RequestHandler):
    def get(self, key_str):
        student_root = self.request.get('student_root', DEFAULT_ROOT)
        # student = Student.get_by_id(int(student_id), parent=get_key(student_root))
        # student = ndb.Key(urlsafe=key_str).get()
        student = ndb.Key('Student', int(key_str), parent=get_key(student_root)).get()
        print student
        template = JINJA_ENV.get_template('student.html')
        template_values = {
                "student": student
                }
        self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add', AddStudent),
    ('/([-\w]+)', OneStudent)
    ], debug=True)
