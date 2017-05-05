#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField, TextAreaField, SubmitField, IntegerField

class AddHostForm(Form):
    ip = StringField(u'Ip')
    port = IntegerField(u'Port')
    username = StringField(u'Username')
    password = PasswordField(u'Password')
    description = TextAreaField(u'Description')
    status_code = BooleanField(u'Status')
    submit = SubmitField(u'Add')

