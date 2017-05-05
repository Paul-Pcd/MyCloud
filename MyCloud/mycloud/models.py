# -*- coding: utf-8 -*-
from sqlalchemy import Column
from .extension import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

OK = 0
ERROR = 1
USER_ADMIN = 0
USER_NORMAL = 1

STATUS = {
    OK: 'OK',
    ERROR: 'ERROR',
}

USER_TYPE = {
    USER_ADMIN : 'ADMIN',
    USER_NORMAL : 'USER',
}

class Host(db.Model):

    __tablename__ = 'hosts'

    id = Column(db.Integer, primary_key = True) #Column函数定义一个字段
    ip = Column(db.String(32), nullable = False)
    vm_list = Column(db.Text)
    vm = db.relationship('VM', backref = 'host', lazy = 'dynamic')
    port = Column(db.SmallInteger, default = 22)
    username = Column(db.String(32), default = 'default')
    password = Column(db.String(32), default = 'default')
    description = Column(db.Text)
    status_code = Column(db.SmallInteger, default = OK)

    def __repr__(self):
        return '%r' %(self.description)


class User(db.Model):

    __tablename__ = 'users'

    id = Column(db.Integer, primary_key = True)
    username = Column(db.String(128), nullable=False, unique=True)
    _password = Column('password',db.String(256), nullable=False)
    email = Column(db.String(64))
    description = Column(db.Text)
    islogin = Column(db.Boolean, default=True)
    type_code = Column(db.SmallInteger, default = USER_NORMAL)
    vms = db.relationship('VM', backref='users', lazy='dynamic')
     
    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)
    password = db.synonym('_password',descriptor = property(_get_password,_set_password))

    def check_password(self, password):
        if self.password is None: return False
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.type_code == USER_ADMIN

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(User.username == login).first()
        if user :
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    def __repr__(self):
        return '%r' %(self.description)

class Image(db.Model):

    __tablename__ = 'images'

    id = Column(db.Integer, primary_key = True)
    image_name = Column(db.String(32), default = 'default')
    image_path = Column(db.String(128))
    status_code = Column(db.SmallInteger, default = OK)
    template_id = db.relationship('Template', backref = 'images', lazy = 'dynamic')

    def __repr__(self):
        return '%r'%(self.image_name)


class Template(db.Model):

    __tablename__ = 'templates'

    id = Column(db.Integer, primary_key = True)
    template_name = Column(db.String(32), default='default')
    cpu = Column(db.Integer, default = 1)
    memory = Column(db.Integer, default = 1048576)
    disk = Column(db.Integer, default = '10G')
    image_id = Column(db.Integer, db.ForeignKey('images.id'))
    vm = db.relationship('VM', backref = 'template', lazy = 'dynamic')
    status_code = Column(db.SmallInteger, default = OK)

    def __repr__(self):
        return '%r'%(self.id)

class VM(db.Model):

    __tablename__ = 'vms'

    id = Column(db.Integer, primary_key = True)
    vm_name = Column(db.String(32), default = 'default')

    host_ip = Column(db.String(32), db.ForeignKey('hosts.ip'))

    template_id = Column(db.Integer, db.ForeignKey('templates.id'))
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    create_time = Column(db.DateTime, default = datetime.now())
    vnc_port = Column(db.Integer, default = 0)
    status = Column(db.String(50))

    def __repr__(self):
        return '%r'%(self.vm_name)
