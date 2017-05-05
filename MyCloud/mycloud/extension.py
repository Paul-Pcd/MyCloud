# -*- coding: utf-8 -*-
#初始化flask-sqlalchmey，flask-login及flask-cache插件


from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()	#提供SQL工具包及对象关系映射的插件

from flask.ext.cache import Cache
cache = Cache()		#提供缓存

from flask.ext.login import LoginManager
login_manager = LoginManager()	#提供用户登录管理
