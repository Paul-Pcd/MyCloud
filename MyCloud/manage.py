# -*- coding: utf-8 -*-

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from mycloud import create_app, db, DEFAULT_BLUEPRINTS
from mycloud.models import User, USER_ADMIN, USER_NORMAL

# 创建应用，加入管理
app = create_app(blueprints = DEFAULT_BLUEPRINTS)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

# 初始化数据库，使用python manager.py initdb执行
@manager.command
def initdb():
    db.drop_all()
    db.create_all()
    admin = User(
            username = u'admin',
            password = u'123456',
            islogin = 'True',
            type_code=USER_ADMIN)
    db.session.add(admin)
    db.session.commit()

@manager.command
def run():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    manager.run()

