#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField, BooleanField, IntegerField

class AddImageForm(Form):
    image_name = StringField(u'Image name')
    image_path = StringField(u'Path')
    status_code = BooleanField(u'Status')
    submit = SubmitField(u'Add')

