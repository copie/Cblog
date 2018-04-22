from datetime import datetime

from flask import abort, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from . import main
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Permission, Post, Role, User


@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           posts=posts)


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
    print(username)
    user = User.query.filter_by(username=username).first()
    print(user)
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
