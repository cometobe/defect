from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from myblog import create_app
from myblog.controllers.model import *
from myblog.exts import db, myconfig

app = create_app(myconfig)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("runserver", Server(host='127.0.0.1', port='8080'))
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag, Role=Role, Devtable=Devtable,
                DevDefect=DevDefect, HiddenPeril=HiddenPeril, Image=Image, BLOGImage=BLOGImage)


if __name__ == "__main__":
    manager.run()
