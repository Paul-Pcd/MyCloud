#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import Form
from wtforms import SubmitField, StringField, BooleanField, IntegerField

class AddVMForm(Form):
    vm_name = StringField(u'VM name')
    template_id = IntegerField(u'Template id')
    host_ip = StringField(u'Host ip')
    submit = SubmitField(u'Add')
