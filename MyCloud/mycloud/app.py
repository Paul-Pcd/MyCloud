# -*- coding: utf-8 -*-

import os

from flask import Flask, request, render_template
from .config import DefaultConfig
from .frontend import frontend
from .extension import db, cache, login_manager
from .user import user
from .host import host
from .image import image
from .template import template
from .vm import vm
from .models import User

__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    user,
    host,
    frontend,   
    image,
    template,
    vm
)

# 创建一个Flask实例并初始化
def create_app(config=None, app_name=None, blueprints=None):

    if app_name is None:
        app_name = DefaultConfig.PROJECT

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    # 创建一个Flask应用实例
    app = Flask(app_name)
    # 使用默认配置（config.py模块）
    configure_app(app, config)	
    # 启用扩展插件（extension.py）
    configure_extension(app)
    # 把应用分解成蓝图的集合（views.py）并注册，每个blueprints对应一个URL
    configure_blueprints(app, blueprints)

    return app

# 配置实例
def configure_app(app, config=None):
    # 启用config.py的配置类
    app.config.from_object(DefaultConfig)

# 启用扩展插件
def configure_extension(app):
    # flask-sqlalchemy
    db.init_app(app)

    # flask-cache
    cache.init_app(app)

    # flask-login
    login_manager.login_view = 'frontend.login'
    login_manager.init_app(app)
    login_manager.setup_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
