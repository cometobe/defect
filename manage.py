from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from myblog import create_app
from myblog.controllers.model import User,Role,HiddenPeril,Detal,Devtable,Comment,BLOGImage,Tag,Post,Image,Devdefect
from myblog.exts import db, myconfig

app = create_app(myconfig)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("runserver", Server(host='127.0.0.1', port='8080'))
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag, Role=Role, Devtable=Devtable,
                HiddenPeril=HiddenPeril, Image=Image, BLOGImage=BLOGImage,Devdefect=Devdefect)

@app.before_first_request
def init_db():
    # db.create_all()
    role1 = Role.query.filter(Role.name=='default').all()
    if not role1:
        role1 = Role(name='default')
        db.session.add(role1)
    role2 = Role.query.filter(Role.name=='admin').all()
    if not role2:
        role2 = Role(name='admin')
        db.session.add(role2)
    detal1 = Detal.query.filter(Detal.title=='defecttime').all()
    if not detal1:
        detal1 = Detal(title='defecttime',content='20170101')
        db.session.add(detal1)
    detal2 = Detal.query.filter(Detal.title=='periltime').all()
    if not detal2:
        detal2 = Detal(title='periltime', content='20170101')
        db.session.add(detal2)
    db.session.commit()




if __name__ == "__main__":
    manager.run()
