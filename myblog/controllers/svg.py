import json

from flask import render_template, Blueprint
from flask_login import login_required, current_user

from myblog.controllers.model import Devtable, UserEncoder

svg_blueprint = Blueprint('svg', __name__, template_folder='templates/svg', static_folder='static', url_prefix="/svg")


# 视图函数
@svg_blueprint.route('/diagram/')
@login_required
def diagram():
    tables = Devtable.query.all()
    devtables = json.dumps(tables, cls=UserEncoder)
    return render_template('svg/svg.html', devinfo=devtables, user=current_user)
