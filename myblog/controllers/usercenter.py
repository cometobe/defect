import os

from PIL import Image
from flask import Blueprint, url_for, redirect, flash, render_template, session, request, make_response, current_app
from flask_login import login_required, current_user, login_user, logout_user
from flask_principal import (Identity, AnonymousIdentity, identity_changed)
from werkzeug.utils import secure_filename

from myblog.controllers import validatecode
from myblog.controllers.forms import loginForm, RegisterForm
from myblog.controllers.model import User
from myblog.exts import db, myconfig, oid

user_blueprint = Blueprint('user', __name__, template_folder='templates/user', static_folder='static',
                           url_prefix="/user")


@user_blueprint.route('/VerifyCode')
def get_verify_code():
    # 把strs发给前端,或者在后台使用session保存
    # code_img, code_text = utils.generate_verification_code()
    code_img, code_text = validatecode.generate_verification_code()
    session['code_text'] = code_text
    response = make_response(code_img)
    response.headers['Content-Type'] = 'image/jpeg'
    print(code_text)
    return response


# ,redirect(url_for('login.get_verify_code'))
@user_blueprint.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
def login():
    form = loginForm()
    if request.method == 'GET':
        return render_template("user/login.html", form=form)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        verifycode = request.form.get('verification_code')
        remember = request.form.get('remember')
        user = User.query.filter_by(username=username).first()
        if user == None:
            flash("密码或者用户名错误", category="success")
            return redirect(url_for('user.login', form=form))
        else:
            if user.check_password(password) == False:
                flash("密码或者用户名错误", category="success")
                return redirect(url_for('user.login', form=form))
            else:
                if 'code_text' in session and session['code_text'] != verifycode:
                    flash("验证码错误", category="success")
                    print(session['code_text'], verifycode)
                    code_img, code_text = validatecode.generate_verification_code()
                    session['code_text'] = code_text
                    return redirect(url_for('user.login', form=form, code_img=code_img))
                else:
                    login_user(user, remember=remember)
                    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
                    # print(current_app, login_user)
                    # flash("登录成功", category="success")
        return redirect(url_for('blog.home'))
        # code_img, code_text = validatecode.generate_verification_code()
        # session['code_text'] = code_text
        # return render_template('login.html', form=form, code_img=code_img)


@user_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )
    flash("注销成功", category="success")
    return redirect(url_for('blog.home'))


@user_blueprint.route('/register', methods=['GET', 'POST'])
@oid.loginhandler
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('user/register.html', form=form)
    else:
        username = request.form.get("username")
        print(username)
        password1 = request.form.get('password')
        password2 = request.form.get('confirmpassword')
        verifycode = request.form.get('verification_code')
        print(password1)
        user = User.query.filter(User.username == username).first()
        print(user)
        if user:
            flash(u"该用户已存在")
            return redirect(url_for('user.register'))
        else:
            if password1 != password2:
                flash(u"密码不一致")
                return redirect(url_for('user.register'))
            else:
                if 'code_text' in session and session['code_text'] != verifycode:
                    flash("验证码错误", category="success")
                    print(session['code_text'], verifycode)
                    code_img, code_text = validatecode.generate_verification_code()
                    session['code_text'] = code_text
                    return redirect(url_for('user.login', form=form, code_img=code_img))
                else:
                    new_user = User(username, password1)
                    new_user.username = username
                    new_user.set_password(password1)
                    # user = User(username=username,password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    flash("注册成功", category="success")
                    return redirect(url_for('user.login'))


@user_blueprint.route('/usercenter', methods=['GET', 'POST'])
@login_required
def usercenter():
    if request.method == 'GET':
        return render_template('user/changepassword.html', user=current_user)
    else:
        password1 = request.form.get("password1")
        password2 = request.form.get('password2')
        password3 = request.form.get('password3')
        passwordcheck = User.query.filter(User.password != password1).first()
        if passwordcheck:
            flash(u"原密码错误")
            return redirect(url_for('usercenter'))
        else:
            if password2 != password3:
                flash(u"密码不一致")
                return redirect(url_for('usercenter'))
            else:
                currentuser = User.query.filter(User.username == current_user.username).first()
                currentuser.password = password2
                db.session.commit()
                flash(u"修改成功")
                return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in myconfig.ALLOWED_IMAGES


@user_blueprint.route('/change_profile', methods=['GET', 'POST'])
@login_required
def change_profile():
    form = loginForm()
    if request.method == 'GET':
        return render_template('user/uploadprofile.html', user=current_user, form=form)
    if request.method == 'POST':
        file = request.files['file']
        user = User.query.filter(User.username == current_user.username).first()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_dir = os.path.join(os.path.curdir, 'myblog/static', myconfig.AVATAR_FOLDER)
            size = (200, 200)
            thumbnailsize = (10,10)
            image = Image.open(file)
            image.thumbnail(size)
            filename = secure_filename(file.filename)
            image.save(os.path.join(save_dir, filename))
            user.head_url = filename

            thumb = Image.open(file)
            thumb.thumbnail(thumbnailsize)
            thumb.save(os.path.join(save_dir, 'Thumbnail' + filename))
            thumbnail_url='Thumbnail'+filename
            user.thumbnail_url=thumbnail_url
            db.session.add(user)
            db.session.commit()
        if request.form.get("motto"):
            user.motto=request.form.get("motto")
            db.session.add(user)
            db.session.commit()
    return redirect(url_for('blog.home'))
