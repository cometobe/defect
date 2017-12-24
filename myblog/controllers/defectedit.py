import tablib,xlrd,os,re
from flask import render_template, redirect, url_for, g, make_response, Blueprint,request,flash
from flask_login import login_required, current_user
from myblog.controllers.forms import defectForm, perilForm
from myblog.controllers.model import Devdefect, Devtable, HiddenPeril,Detal
from myblog.exts import db,myconfig
from datetime import datetime

defect_blueprint = Blueprint('defect', __name__, template_folder='templates/defect', static_folder='static',
                             url_prefix="/defecta")


# 缺陷表格数据

def open_excel(file='file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def excel_table_byindex(file= 'file.xls',colnameindex=1,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(2,nrows):
        row = table.row_values(rownum)
        if row:
            cols = {}
            for i in range(len(colnames)):
                # print(row[i])
                cols[colnames[i]] = row[i]
            list.append(cols)
    # print(list)
    return list

ALLOWED_EXTENSIONS = (['xls', 'xlsx'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def writedefectdata(defect,row):
    defect.voltageGrade = row['电压等级']
    defect.defectGrade = row['缺陷等级']
    defect.defectStation = row['地点']
    defect.defectPlace = row['功能位置']
    defect.defectDev = row['设备名称']
    defect.defectPart = row['部件名称']
    defect.defectCause = row['缺陷类型']
    defect.deviceCategory = row['设备类别']
    defect.deviceCategoryId = row['设备类别编码']
    defect.defectPhan = row['缺陷表象']
    defect.defectDescription = row['缺陷描述']
    defect.defectState = row['缺陷状态']
    defect.professionCategory1 = row['专业大类']
    defect.professionCategory2 = row['专业小类']
    defect.deadTime = row['应完成缺陷处理时间']
    defect.defectFindTime = row['发现时间']
    defect.defectFindPerson = row['发现人']
    defect.defectRemoveTime = row['消缺时间']
    defect.defectRemoveTeam = row['消缺班组']
    defect.defectRemovePerson = row['消缺人']
    defect.defectReason = row['缺陷原因']
    defect.defectPart2 = row['缺陷部位']
    defect.defectRemoveMethod = row['处理措施']
    defect.defectRemoveMethodDetal = row['处理情况描述']
    defect.defectCheckTime = row['验收时间']
    defect.defectCheckPerson = row['验收人']
    defect.defectManufacturer = row['生产厂家']
    defect.deviceProductDate = row['出厂年月']
    defect.deviceModelNo = row['设备型号']
    defect.deviceCommissionDate = row['投运日期']

def writeperildata(peril,row):
    peril.perilId = row['隐患编号']
    peril.perilStation = row['填报单位']
    # peril.perilVolt = row['缺陷等级']
    peril.perilTitle = row['隐患名称']
    # peril.perilPart = row['功能位置']
    peril.perilLocal = row['隐患地点']
    peril.perilDescription = row['隐患描述']
    peril.perilFrom = row['隐患来源']
    peril.perilCategory1 = row['隐患一级类型']
    peril.perilCategory2 = row['隐患二级类型']
    peril.perilCategory3 = row['隐患二级类型']
    peril.perilFindTime = row['隐患发现日期']
    peril.perilEvaTime = row['隐患评估日期']
    peril.perilGrade = row['隐患等级']
    peril.perilCause = row['隐患后果']
    peril.perilCauseGrade = row['隐患后果等级']
    peril.perilRemoveTeam = row['治理责任单位']
    peril.perilPlan = row['隐患整治初步方案']
    peril.perilState = row['状态']
    peril.perilSupervise = row['督办信息']


@defect_blueprint.route('/defectdisplay/', methods=['GET', 'POST'])
@login_required
def defectdisplay():
    # form = defectuploadForm()
    defects = Devdefect.query.filter(Devdefect.defectState != "已归档").all()
    perils = HiddenPeril.query.filter(HiddenPeril.perilState != "已结束").all()
    timed = Detal.query.filter(Detal.title == 'defecttime').first()
    timep = Detal.query.filter(Detal.title == 'periltime').first()
    if request.method == 'POST':
        save_dir = os.path.join(os.path.curdir, 'myblog\static', myconfig.UPLOAD_FOLDER,'excel')
        # print(save_dir)
        file = request.files['file']
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = current_user.username+'_'+time+'_'+file.filename

        # 判断文件名是否合规
        if file and allowed_file(filename) and 'DefectExcelExportTemplate' in filename:
            file.save(os.path.join(save_dir,filename))
            flash('成功:缺陷数据文件已上传服务器')
            defecttime = re.search(r"e_(\d.+).xls", file.filename).group(1)
            timed.content = defecttime[:10]
            db.session.add(timed)
            db.session.commit()
            tables = excel_table_byindex(file=os.path.join(save_dir, filename))
            for row in tables:
                # print(row)
                defect = Devdefect.query.filter(Devdefect.defectId == row['缺陷编号']).first()
                if defect:
                    writedefectdata(defect, row)
                    db.session.commit()
                elif row['地点'] == '±500kV安顺换流站':
                    newdefect = Devdefect(defectId=row['缺陷编号'])
                    writedefectdata(newdefect, row)
                    db.session.add(newdefect)
                    db.session.commit()
                else:pass
            redirect(url_for('defect.defectdisplay'))
        elif file and allowed_file(filename) and '安全隐患' in filename:
            file.save(os.path.join(save_dir, filename))
            flash('成功:隐患数据文件已上传服务器')
            periltime = re.search(r"患_(\d.+).xls", file.filename).group(1)
            timep.content =periltime[:10]
            db.session.add(timep)
            db.session.commit()
            tables = excel_table_byindex(file=os.path.join(save_dir, filename))
            for row in tables:
                peril = HiddenPeril.query.filter(HiddenPeril.perilId == row['隐患编号']).first()
                if peril:
                    writeperildata(peril, row)
                    db.session.commit()
                elif '安顺换流站'in row['填报单位']:
                    newperil = HiddenPeril(perilId=row['隐患编号'])
                    writeperildata(newperil, row)
                    db.session.add(newperil)
                    db.session.commit()
                else:pass
            redirect(url_for('defect.defectdisplay'))
        else:
            flash('失败:上传文件格式不对')
            redirect(url_for('defect.defectdisplay'))
    return render_template('defect/defectdisplay.html', defects=defects, perils=perils, user=current_user,
                           timed=timed,timep=timep
                           )


@defect_blueprint.route('/defectedit/<defectid>', methods=['GET', 'POST'])
@login_required
def defectedit(defectid):
    defectitem = Devdefect.query.filter(Devdefect.defectId == defectid).first()
    devfind = Devtable.query.filter(Devtable.devname == defectitem.defectDev).first()
    form = defectForm()
    if form.validate_on_submit():
        if g.user.userprivilege <= 2:
            if form.defectcause.data:
                defectitem.defectCause = form.defectcause.data
            if form.defectshortaction.data:
                defectitem.shortAction = form.defectshortaction.data
            if form.defectshorttime.data:
                defectitem.shortTime = form.defectshorttime.data
            if form.defectmiddleaction.data:
                defectitem.middleAction = form.defectmiddleaction.data
            if form.defectmiddletime.data:
                defectitem.middleTime = form.defectmiddletime.data
            if form.defectlongaction.data:
                defectitem.longAction = form.defectlongaction.data
            if form.defectlongtime.data:
                defectitem.longTime = form.defectlongtime.data
            if form.defectremoveteam.data:
                defectitem.defectRemoveTeam = form.defectremoveteam.data
            defectitem.workHaveDone = form.defectwork.data
            while form.defectmas.data:
                devmaster = form.defectmas.data
                defectitem.deviceMaster = devmaster
                break
            while devfind:
                devmaster = devfind.devmas
                defectitem.deviceMaster = devmaster
                break
            db.session.commit()
        return redirect(url_for('.defectdisplay'))
    else:
        return render_template('defect/edit.html', form=form, defectitem=defectitem, user=current_user)


@defect_blueprint.route('/periledit/<perilId>', methods=['GET', 'POST'])
@login_required
def periledit(perilId):
    perilitem = HiddenPeril.query.filter(HiddenPeril.perilId == perilId).first()
    form = perilForm()
    if form.validate_on_submit():
        if g.user.userprivilege <= 2:
            if form.perilTitle.data:
                perilitem.perilTitle = form.perilTitle.data
            if form.perilPart.data:
                perilitem.perilPart = form.perilPart.data
            if form.perilcause.data:
                perilitem.perilCause = form.perilcause.data
            if form.perilVolt.data:
                perilitem.perilVolt = form.perilVolt.data
            if form.perilshortaction.data:
                perilitem.shortAction = form.perilshortaction.data
            if form.perilshorttime.data:
                perilitem.shortTime = form.perilshorttime.data
            if form.perilmiddleaction.data:
                perilitem.middleAction = form.perilmiddleaction.data
            if form.perilmiddletime.data:
                perilitem.middleTime = form.perilmiddletime.data
            if form.perillongaction.data:
                perilitem.longAction = form.perillongaction.data
            if form.perillongtime.data:
                perilitem.longTime = form.perillongtime.data
            if form.perilremoveteam.data:
                perilitem.perilRemoveTeam = form.perilremoveteam.data
            perilitem.workHaveDone = form.perilwork.data
            if form.perilmas.data:
                perilitem.deviceMaster = form.perilmas.data
            db.session.commit()
        return redirect(url_for('.defectdisplay'))
    else:
        return render_template('defect/editperil.html', form=form, perilitem=perilitem, user=current_user)


@defect_blueprint.route('/defectexcel', methods=['GET', 'POST'])
def defectexcel():
    defectquery = Devdefect.query.filter(Devdefect.defectState != "已归档")
    defects = defectquery.all()
    long = defectquery.count()

    perilquery = HiddenPeril.query.filter(HiddenPeril.perilState != "已结束")
    perils = perilquery.all()
    perillong = perilquery.count()

    headers = (u"序号", u"电压等级", u"设备名称", u"设备部件", u"缺陷隐患描述", u"缺陷隐患后果", u"缺陷隐患等级", u"发现时间",
               u"短期控制措施", u"完成时间", u"中期控制措施", u"完成时间", u"长期控制措施", u"完成时间", u"消缺班组", u"负责人", u"月度完成情况")

    rows = []
    for i in range(0, long):
        rows.append([i + 1])
        rows[i].append(defects[i].voltageGrade)
        rows[i].append(defects[i].defectDev)
        if defects[i].defectPart:
            rows[i].append(defects[i].defectPart)
        else:
            rows[i].append("")
        rows[i].append(defects[i].defectDescription)
        if defects[i].defectCause:
            rows[i].append(defects[i].defectCause)
        else:
            rows[i].append("")
        rows[i].append(defects[i].defectGrade)
        rows[i].append(defects[i].defectFindTime)
        if defects[i].shortAction:
            rows[i].append(defects[i].shortAction)
        else:
            rows[i].append("")
        if defects[i].shortTime:
            rows[i].append(defects[i].shortTime)
        else:
            rows[i].append("")
        if defects[i].middleAction:
            rows[i].append(defects[i].middleAction)
        else:
            rows[i].append("")
        if defects[i].middleTime:
            rows[i].append(defects[i].middleTime)
        else:
            rows[i].append("")
        if defects[i].longAction:
            rows[i].append(defects[i].longAction)
        else:
            rows[i].append("")
        if defects[i].longTime:
            rows[i].append(defects[i].longTime)
        else:
            rows[i].append("")
        if defects[i].defectRemoveTeam:
            rows[i].append(defects[i].defectRemoveTeam)
        else:
            rows[i].append("")
        if defects[i].deviceMaster:
            rows[i].append(defects[i].deviceMaster)
        else:
            rows[i].append("")
        if defects[i].workHaveDone:
            rows[i].append(defects[i].workHaveDone)
        else:
            rows[i].append("")

    for i in range(0, perillong):
        rows.append([i + long + 1])
        rows[long + i].append(perils[i].perilVolt)
        rows[long + i].append(perils[i].perilTitle)
        if perils[i].perilPart:
            rows[long + i].append(perils[i].perilPart)
        else:
            rows[long + i].append("")
        rows[long + i].append(perils[i].perilDescription)
        if perils[i].perilCause:
            rows[long + i].append(perils[i].perilCause)
        else:
            rows[long + i].append("")
        rows[long + i].append(perils[i].perilGrade)
        rows[long + i].append(perils[i].perilFindTime)
        if perils[i].shortAction:
            rows[long + i].append(perils[i].shortAction)
        else:
            rows[long + i].append("")
        if perils[i].shortTime:
            rows[long + i].append(perils[i].shortTime)
        else:
            rows[long + i].append("")
        if perils[i].middleAction:
            rows[long + i].append(perils[i].middleAction)
        else:
            rows[long + i].append("")
        if perils[i].middleTime:
            rows[long + i].append(perils[i].middleTime)
        else:
            rows[long + i].append("")
        if perils[i].longAction:
            rows[long + i].append(perils[i].longAction)
        else:
            rows[long + i].append("")
        if perils[i].longTime:
            rows[long + i].append(perils[i].longTime)
        else:
            rows[long + i].append("")
        if perils[i].perilRemoveTeam:
            rows[long + i].append(perils[i].perilRemoveTeam)
        else:
            rows[long + i].append("")
        if perils[i].deviceMaster:
            rows[long + i].append(perils[i].deviceMaster)
        else:
            rows[long + i].append("")
        if perils[i].workHaveDone:
            rows[long + i].append(perils[i].workHaveDone)
        else:
            rows[long + i].append("")

    data = tablib.Dataset(*rows, headers=headers)

    resp = make_response(data.xlsx)
    resp.headers["Content-Disposition"] = "attachment; filename=defecttrack.xlsx"
    return resp
