from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from wtforms import BooleanField
from . import manage
from .. import db
from .. decorators import admin_required, permission_required
from .. models import Post, Role, Tag, User
from . forms import (EditProfileAdminForm, EditProfileForm, DelTagForm,
                     PostForm, AddTagForm)


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


def select_sql(tag):
    tmp = Tag.query.filter_by(tag=tag).first()
    if tmp:
        return tmp
    return None


@manage.route('/manage/tags', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_tags():
    form_one = AddTagForm()
    form_list = DelTagForm()
    if request.args.get('do') == 'del':
        if form_list.validate_on_submit():
            list(map(db.session.delete, map(
                select_sql, form_list.tags.data.split(','))))
            db.session.commit()

    if request.args.get('do') == 'add':
        if form_one.validate_on_submit():
            tag = Tag()
            tag.tag = form_one.tag.data
            db.session.add(tag)
            db.session.commit()

    tags = (x.tag for x in Tag.query.filter_by().all())
    return render_template('manage/tags.html',
                           form_one=form_one, form_list=form_list, tags=tags)
