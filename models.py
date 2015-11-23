# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


class Student(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    registration = ndb.StringProperty(indexed=False)
    department = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def student_id(self):
        return self.key.id()
