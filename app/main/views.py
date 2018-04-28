from datetime import datetime

from flask import abort, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from . import main
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Permission, Post, Role, User, Tag, Classify


def info_list():
    info_list = {}
    info_list['tags_amount'] = len(Tag.query.all())
    info_list['classifys_amount'] = len(Classify.query.all())
    info_list['blog_amount'] = len(Post.query.all())
    info_list['all_page'] = info_list['blog_amount']+1
    return info_list


@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for("main.page", num=1))


@main.route('/test')
@login_required
def test():
    return "这个页面只有登陆过的人才可以看到"


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "只有管理员可以看见这个页面偶"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('main/user.html', user=user)


@main.route('/tags')
def tags():
    tags = map(lambda x: x.tag, Tag.query.all())
    return render_template('main/tags.html', tags=tags, info_list=info_list())


@main.route('/tag/<tag>')
def tag(tag):
    return tag


@main.route('/posts')
def posts():
    '''文章归档'''
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('main/posts.html', posts=posts, info_list=info_list())


@main.route('/page/<int:num>')
def page(num):
    # 博客分页,每页7个,注意当 num = 0 时会出现[3,4...,11]
    n = 7
    posts = Post.query.order_by(Post.timestamp.desc()).all()[
        (num - 1) * n: num * n - 1]
    posts_len = int(len(Post.query.all())/n)+1
    num_list = range(1 if num < 5 else num-4,
                     posts_len+1 if num > posts_len - 5 else num + 4)
    print(num_list)
    return render_template('main/index.html', info_list=info_list(),
                           posts=posts, num=num, num_list=num_list)

@main.route('/post/<int:id>.html')
def post(id):
    '''文章的具体内容'''
    post = Post.query.get_or_404(id)
    return render_template('main/post.html', post=post, info_list=info_list())
