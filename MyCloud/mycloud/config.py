# -*- coding: utf-8 -*-

import os

#默认配置类，由app.py的configure_app(app, config)函数调用对Flask应用app进行配置
class DefaultConfig(object):

    PROJECT = "mycloud"

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    #用于修改session（相当于密钥签名加密的cookie，在服务端记录信息确认用户身份）的密钥
    SECRET_KEY = '~!@@#@WERW'

    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = True

    # MYSQL for production.
    #SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db?charset=utf8'

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60	#flask cache类型，提高页面加载速度

    SQLALCHEMY_DATABASE_URI = "mysql://user1:123456@SharedStorage/mycloud"
    
