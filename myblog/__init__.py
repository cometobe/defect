import re
from flask import Flask, redirect, url_for,session,request
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from myblog.controllers.model import User,Role,HiddenPeril,Detal,Devtable,Comment,BLOGImage,Tag,Post,Image,Devdefect
from myblog.controllers.admin import MyModelView,MyFileView,MyView
from myblog.exts import db, bcrypt, oid, login_manager, principals, bootstrap,admin
from .controllers.blog import blog_blueprint
from .controllers.dataman import data_blueprint
from .controllers.defectedit import defect_blueprint
from .controllers.svg import svg_blueprint
from .controllers.table import table_blueprint
from .controllers.usercenter import user_blueprint

import os.path as op
path = op.join(op.curdir, 'myblog/static')


def str2list(str):
    liststr = re.findall(r"'(.+?)'", str)
    return liststr


def poster(self):
    post = User.query.filter_by(id=self.Userid).first()
    poster = post.username
    return poster

def postheadurl(self):
    poster = User.query.filter_by(id=self.Userid).first()
    postheadurl = poster.thumbnail_url
    return postheadurl



#
# def custom_email(form,field):
#     if not re.match(r"[^@]+@[^@]+\.[^@]+",field.data):
#         raise wtforms.ValidationError('Field must be a valid email address')



def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)

    models = [User,Role,HiddenPeril,Detal,Devtable,Comment,BLOGImage,Tag,Post,Image,Devdefect]

    for model in models:
        admin.add_view(MyModelView(model,db.session,category='models'))
    admin.add_view(MyFileView(path, '/static/', name='Static Files'))
    admin.add_view(MyView(name='链接'))

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'userrole'):
            for role in current_user.userrole:
                # print(role)
                identity.provides.add(RoleNeed(role.name))
                # print(identity)

    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    app.register_blueprint(blog_blueprint, url_prefix='/blog')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(data_blueprint, url_prefix='/data')
    app.register_blueprint(table_blueprint, url_prefix='/table')
    app.register_blueprint(svg_blueprint, url_prefix='/svg')
    app.register_blueprint(defect_blueprint, url_prefix='/defect')


    @app.errorhandler(403)
    def page_not_found(e):
        session['redirected_from'] = request.url
        return redirect(url_for('user.login'))

    env = app.jinja_env
    env.filters['str2list'] = str2list
    env.filters['poster'] = poster
    env.filters['postheadurl'] = postheadurl


    return app
