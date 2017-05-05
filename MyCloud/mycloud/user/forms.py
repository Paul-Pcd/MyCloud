#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import Form
from wtforms import TextAreaField, PasswordField, StringField, RadioField, BooleanField, TextField, SubmitField, IntegerField

class AddUserForm(Form):
    
    username = StringField(u'Username') 
    #password = PasswordField(u'Password', validators=[DataRequired('Cannot be null!')]) 
    password = PasswordField(u'Password')
    email = StringField(u'E-mail')
    description = TextAreaField(u'Description')
    islogin = BooleanField(u'IsLogin?')
    type_code = RadioField(u'UserType', choices=[('1','Normal'),('0','Admin')], default = '1')
    submit = SubmitField(u'Add')
    
    def save (self):
        user = User()
        user.username = self.username.data
        user.password = self.password.data
        user.email = self.email.data
        user.description = self.description.data
        user.islogin = self.islogin.data
        user.type_code = self.username.data
        return user.save()
'''
class ChangeUserForm(Form):
    
    username = StringField(u'Username')
#    password = PasswordField(u'Password', validators=[DataRequired('Cannot be null!')])
    password = PasswordField(u'Password')
    password2 = PasswordField(u'Confirm')
    email = StringField(u'E-mail')
    description = TextAreaField(u'Description')
    islogin = BooleanField(u'IsLogin?')
    submit = SubmitField(u'Add')
    
    def save(self, user_id):
        user = User.query.get_or_404(user_id)
        user.username = self.username.data
        user.email = self.email.data
        user.description = self.description.data
        if self.password.data:
            user.password = self.password.data
        return user.save()

    def save_all(self, user_id):
        user = User.query.get_or_404(user_id)
        user.username = self.username.data
        user.email = self.email.data
        user.description = self.description.data
        user.islogin = self.islogin.data
        if self.password.data:
            user.password = self.password.data
        return user.save()

'''
