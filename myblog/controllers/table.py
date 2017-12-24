from flask import render_template, request, Blueprint
from flask_login import login_required, current_user

from myblog.controllers.model import Devtable

table_blueprint = Blueprint('table', __name__, template_folder='templates/table', static_folder='static',
                            url_prefix="/table")


# 设备主人表格数据

@table_blueprint.route('/master', methods=['GET', 'POST'])
@login_required
def mastertable():
    q1 = request.form.get('devclass')
    q2 = request.form.get('devname')
    q3 = request.form.get('devmas')
    q4 = request.form.get('devManageGrade')
    q5 = request.form.get('devHealth')
    q6 = request.form.get('devImportance')
    if q1 or q2 or q3 or q4 or q5 or q6:
        tables = {
            'devtable': Devtable.query.filter(Devtable.devclass.contains(q1),
                                              Devtable.devname.contains(q2),
                                              Devtable.devmas.contains(q3),
                                              Devtable.devManageGrade.contains(q4),
                                              Devtable.devHealth.contains(q5),
                                              Devtable.devImportance.contains(q6)).all()
        }
    else:
        tables = {
            'devtable': Devtable.query.all()
        }
    return render_template('table/master.html', **tables, user=current_user)
