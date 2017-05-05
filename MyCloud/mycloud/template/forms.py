#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField, BooleanField, IntegerField

class AddTemplateForm(Form):
    template_name = StringField(u'Template name')
    cpu = StringField(u'CPU')
    memory = StringField(u'Memory')
    disk = StringField(u'Disk')
    image_id = IntegerField('Image id')
    status_code = BooleanField(u'Status')
    submit = SubmitField(u'Add')

class ModifyTemplateForm(Form):
    cpu = StringField(u'CPU')
    memory = StringField(u'Memory')
    disk = StringField(u'Disk')
    image_id = IntegerField('Image id')
    status_code = BooleanField(u'Status')
    submit = SubmitField(u'Add')
