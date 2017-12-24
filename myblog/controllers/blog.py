import datetime
import os,json
from PIL import Image
from flask import render_template, Blueprint, redirect, url_for, abort, request
from flask_login import current_user,login_required
from flask_principal import UserNeed
from sqlalchemy import func
from werkzeug.utils import secure_filename

from myblog.controllers.forms import CommentForm, PostForm
from myblog.controllers.model import Post, Tag, tags, Comment, User
from myblog.exts import db, poster_permission, admin_permission, Permission, myconfig

blog_blueprint = Blueprint('blog', __name__, template_folder='templates/blog', static_folder='static/bolg',
                           url_prefix="/blog")


def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(10).all()
    top_tags = db.session.query(Tag, func.count(tags.c.postid).label('total')) \
        .join(tags).group_by(Tag).order_by('total DESC').all()

    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
    postpages = posts.items
    recent, top_tags = sidebar_data()
    # 随机生成文章
    # user = User.query.get(1)
    # tag_one = Tag('Python')
    # tag_two = Tag('Flask')
    # tag_three = Tag('SQLAlechemy')
    # tag_four = Tag('jinja')
    # tag_list = [tag_one, tag_two, tag_three, tag_four]
    #
    # s = "example text"
    #
    # for i in range(100):
    #     new_post = Post('Post' + str(i))
    #     new_post.user = user
    #     new_post.publish_date = datetime.datetime.now()
    #     new_post.text = s
    #     new_post.tags = random.sample(tag_list, random.randint(1, 3))
    #     db.session.add(new_post)
    #
    # db.session.commit()

    # user = User.query.filter_by(id =post.Userid).first()
    # if user:
    #     username = user.username

    uploaddir = myconfig.UPLOAD_FOLDER
    avatardir = myconfig.AVATAR_FOLDER
    return render_template('blog/home.html',
                           posts=posts,
                           postpages=postpages,
                           recent=recent,
                           top_tags=top_tags,
                           user=current_user,
                           uploaddir=uploaddir,
                           avatardir=avatardir
                           )


@blog_blueprint.route('/post/<int:postid>', methods=('GET', 'POST'))
def post(postid):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.postid = postid
        new_comment.date = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
    post = Post.query.get_or_404(postid)
    tags = post.tags
    publish_date = post.publish_date
    user = User.query.filter_by(id=post.Userid).first()
    if user:
        username = user.username
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()
    uploaddir = myconfig.UPLOAD_FOLDER
    # if post.postimage_url[0] is not None:
    #     url =post.postimage_url[0]
    # else:
    #     url =url_for('static',filename='/avatardir/default.png')
    return render_template('blog/post.html',
                           post=post,
                           username=username,
                           publish_date=publish_date,
                           tags=tags,
                           comments=comments,
                           recent=recent,
                           top_tags=top_tags,
                           form=form,
                           user=current_user,
                           uploaddir=uploaddir,
                           # url=url
                           )


@blog_blueprint.route('/tag/<string:tag_name>')
@login_required
def tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    post = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('blog/Tag.html',
                           post=post,
                           tag=tag,
                           recent=recent,
                           top_tags=top_tags,
                           user=current_user
                           )


@blog_blueprint.route('/user/<string:username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    post = user.posts.order_by(
        Post.publish_date.desc()
    ).all()
    recent, top_tags = sidebar_data()

    return render_template('blog/user.html',
                           post=post,
                           user=user,
                           recent=recent,
                           top_tags=top_tags
                           )


@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.query.get_or_404(id)

    if not current_user:
        return redirect(url_for('log.login'))
    if current_user != post.users:
        return redirect(url_for('blog.post', postid=id))
    permission = Permission(UserNeed(post.Userid))
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()

            db.session.add(post)
            db.session.commit()

            return redirect(url_for('.post', postid=post.id))
        form.text.data = post.text
        return render_template('blog/edit.html', form=form, post=post, user=current_user)
    abort(403)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in myconfig.ALLOWED_EXTENSIONS


# def save_to_local(file, file_name):
#     save_dir = os.path.join(os.getcwd(), ProdConfig.UPLOAD_FOLDER)
#     file.save(os.path.join(save_dir, file_name))
#     return '/image/' + file_name

@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """View function for new_port."""
    form = PostForm()
    # print(form.validate_on_submit(),request.method == 'POST')
    if form.validate_on_submit():
        new_post = Post(title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()
        new_post.Userid = current_user.id
        # add image
        save_dir = os.path.join(os.path.curdir, 'myblog/static', myconfig.UPLOAD_FOLDER)
        if request.method == 'POST':
            uploaded_files = request.files.getlist("file[]")
            print(uploaded_files)
            filenames = []
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    userfilename = current_user.username+"-"+filename
                    size = (700, 700)
                    im = Image.open(file)
                    im.thumbnail(size)
                    im.save(os.path.join(save_dir, userfilename))
                    filenames.append(userfilename)
                    new_post.postimage_url = str(filenames)

                file1 = uploaded_files[0]
                if file1 and allowed_file(file1.filename):
                    size = (200, 200)
                    im = Image.open(file1)
                    im.thumbnail(size)
                    filename1 = secure_filename(file1.filename)
                    userfilename1 = current_user.username+"-" + filename1
                    im.save(os.path.join(save_dir, 'Thumbnail-' + userfilename1))
                    new_post.postthumbnail_url = userfilename1
        #获取标签
            if request.values.getlist('tags[]'):
                selecttags = request.values.getlist('tags[]')
                # print(selecttags)

                tags = Tag.query.all()
                tagno = Tag.query.count()
                tagnames = []
                for i in range(tagno):
                    tagnames.append(tags[i].name)
                for tag in selecttags:
                    try:
                        tag = int(tag)
                        tagname = tagnames[tag]
                    except:
                        post_tag = add_tags(tag)
                        new_post.tags.append(post_tag)
                    else:
                        tagname = Tag.query.filter(Tag.name==tagname).first()
                        post_tag = add_tags(tagname.name)
                        new_post.tags.append(post_tag)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('blog.home'))
    return render_template('blog/new_post.html', form=form, user=current_user)


@blog_blueprint.route('/taglist', methods=['GET'])
@login_required
def taglist():
    tags = Tag.query.all()
    tagno= Tag.query.count()
    taglist=[]
    for i in range(tagno):
        taglist.append({"id":i,"text":tags[i].name})

    # print(json.dumps(taglist))
    return json.dumps(taglist)


def add_tags(tag):
    existing_tag = Tag.query.filter(Tag.name == tag).one_or_none()
    """if it does return existing tag objec to list"""
    if existing_tag is not None:
        return existing_tag
    else:
        new_tag = Tag(name=tag)
        return new_tag
