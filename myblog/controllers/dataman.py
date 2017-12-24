from flask import render_template, Blueprint
from flask_login import login_required, current_user

from myblog.controllers.model import Devtable

data_blueprint = Blueprint('data', __name__, template_folder='templates/data', static_folder='static',
                           url_prefix="/data")


@data_blueprint.route('/data/')
@login_required
def dashboard():
    d = ["於海", "石永立", "汤勇", "谢辰昱", "朱俊", "项方宇", "田茂熙", "陈泽", "贺强", "罗斌", "张杰", "冯文华", "郭天炜", "侯谭松", "叶露"]
    ff = []
    for i in range(15):
        ff.append(Devtable.query.filter_by(devmas=d[i]).count())
    gg = [[], [], [], []]
    for i in range(15):
        gg[0].append({"name": d[i], "profit": Devtable.query.filter_by(devmas=d[i], devImportance="关键").count()})
        gg[1].append({"name": d[i], "profit": Devtable.query.filter_by(devmas=d[i], devImportance="重要").count()})
        gg[2].append({"name": d[i], "profit": Devtable.query.filter_by(devmas=d[i], devImportance="关注").count()})
        gg[3].append({"name": d[i], "profit": Devtable.query.filter_by(devmas=d[i], devImportance="一般").count()})
    ggj = [{"name": "一般设备", "importance": gg[3]}, {"name": "关注设备", "importance": gg[2]},
           {"name": "重要", "importance": gg[1]}, {"name": "关键设备", "importance": gg[0]}]
    hh = [[], [], [], []]
    for i in range(15):
        hh[0].append({"name": d[i], "profit": Devtable.query.filter_by(devmas=d[i], devManageGrade="1").count()})
        hh[1].append({"name": d[i], "profit": Devtable.query.filter_by(devmas=d[i], devManageGrade="2").count()})
        hh[2].append({"name": d[i], "profit": Devtable.query.filter_by(devmas=d[i], devManageGrade="3").count()})
        hh[3].append({"name": d[i], "profit": Devtable.query.filter_by(devmas=d[i], devManageGrade="4").count()})
    hhj = [{"name": "IV级管控", "importance": hh[3]}, {"name": "III级管控", "importance": hh[2]},
           {"name": "II级管控", "importance": hh[1]}, {"name": "I级管控", "importance": hh[0]}, ]
    return render_template('data/data.html', xd=d, data1=ff, data2=ggj, data3=hhj, user=current_user)
