# -*- coding: utf-8 -*-

#在__init__.py从view.py导出user蓝图，供user目录外部调用（from user import user）
from .views import user
