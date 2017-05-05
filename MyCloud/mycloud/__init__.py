# -*- coding: utf-8 -*-

#在__init__.py导出创建Flask应用的函数，供mycloud目录外部调用（from mycloud import create_app）
from app import create_app, db, DEFAULT_BLUEPRINTS
