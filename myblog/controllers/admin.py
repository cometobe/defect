from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from myblog.exts import db,admin_permission
from flask_admin import BaseView,expose
from flask_login import current_user


#admin
class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom.html')


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and admin_permission.can()

class MyFileView(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and admin_permission.can()

