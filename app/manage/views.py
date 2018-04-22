from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import manage
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Post, Role, User

from .forms import EditProfileAdminForm, EditProfileForm, PostForm


@manage.route('/manage/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    print("asdhasjdhkasj")
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash("你的资料已经修改完成")
        print(current_user.name, current_user.location, current_user.about_me)
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('manage/edit_profile.html', form=form)


@manage.route('/manage/edit-profile/<int:id>', methods=['GET', 'POST'])
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
    return render_template('manage/edit_profile.html', form=form, user=user)


@manage.route('/manage/writeblog', methods=['GET', 'POST'])
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
    return render_template('manage/writeblog.html', form=form)
