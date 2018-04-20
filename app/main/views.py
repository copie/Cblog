from datetime import datetime

from flask import abort, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from . import main
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Permission, Post, Role, User
from .forms import EditProfileAdminForm, EditProfileForm, PostForm


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


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash("你的资料已经修改完成")
        print(current_user.name, current_user.location, current_user.about_me)
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('已经修改完成用户信息')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/writeblog', methods=['GET', 'POST'])
@login_required
@admin_required
def writeblog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('writeblog.html', form=form)
