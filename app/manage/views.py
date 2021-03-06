from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from wtforms import BooleanField

from . import manage
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Classify, Post, Role, Tag, User
from .forms import (AddClassifyForm, AddTagForm, EditProfileAdminForm,
                    EditProfileForm, ManageWithIDs, PostForm)


@manage.route('/manage/edit-profile', methods=['GET', 'POST'])
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
        return redirect(request.args.get('next') or
                        url_for('main.user', username=user.username))

    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('manage/edit_profile.html', form=form, user=user)


@manage.route('/manage/modifyblog/<int:id>', methods=['GET', 'POST'])
@manage.route('/manage/writeblog', methods=['GET', 'POST'])
@login_required
@admin_required
def manageblog(id=None):
    form = PostForm()
    all_tag = list(map(lambda tag: tag.tag, Tag.query.all()))
    all_classify = list(
        map(lambda classify: classify.classify, Classify.query.all()))

    if id is None:
        post = Post()
    else:
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.author = current_user._get_current_object()

        # 删除就标签 添加新标签
        tags = add_tags(form.tags.data)
        tmp = post.tags.all()
        list(map(lambda t: post.tags.remove(t), tmp))
        list(map(lambda t: post.tags.append(t), tags))

        # 删除就分类 添加新分类
        classifys = add_classifys(form.classifys.data)
        tmp = post.classifys.all()
        list(map(lambda c: post.classifys.remove(c), tmp))
        list(map(lambda c: post.classifys.append(c), classifys))
        if id is None:
            db.session.add(post)
            db.session.commit()
            flash("添加文章完成")
            return redirect(url_for('main.index'))
        else:
            db.session.commit()
            flash("修改文章完成")
            return redirect(url_for('manage.manage_posts'))
    if id is not None:
        form.title.data = post.title
        form.body.data = post.body
        form.tags.data = ','.join(map(lambda tag: tag.tag, post.tags.all()))
        form.classifys.data = ','.join(
            map(lambda classify: classify.classify, post.classifys.all()))

    return render_template('manage/manageblog.html', form=form,
                           all_tag=all_tag, all_classify=all_classify)


def select_sql_tag(tag):
    tmp = Tag.query.filter_by(tag=tag).first()
    if tmp:
        return tmp
    return None


def add_tags(tag_str):
    tag_list = tag_str.split(',')
    tags = []
    for tag in tag_list:
        s_tag = select_sql_tag(tag)
        if not s_tag:
            s_tag = Tag()
            s_tag.tag = tag
            db.session.add(s_tag)
        tags.append(s_tag)
    db.session.commit()
    return tags


@manage.route('/manage/tags', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_tags():
    add_tag = AddTagForm()
    del_tag_id = ManageWithIDs(Tag)
    if request.args.get('do') == 'del':
        if del_tag_id.validate_on_submit():
            list(map(db.session.delete, del_tag_id.datas))
            db.session.commit()
        return redirect(url_for('manage.manage_tags'))
    if request.args.get('do') == 'add':
        if add_tag.validate_on_submit():
            tag = Tag()
            tag.tag = add_tag.tag.data
            db.session.add(tag)
            db.session.commit()
        return redirect(url_for('manage.manage_tags'))
    tags = Tag.query.filter_by().all()
    return render_template('manage/tags.html',
                           add_tag=add_tag, id_list=del_tag_id, tags=tags)


def select_sql_classify(classify):
    tmp = Classify.query.filter_by(classify=classify).first()
    if tmp:
        return tmp
    return None


def add_classifys(classify_str):
    classify_list = classify_str.split(',')
    classifys = []
    for classify in classify_list:
        s_classify = select_sql_classify(classify)
        if not s_classify:
            s_classify = Classify()
            s_classify.classify = classify
            db.session.add(s_classify)
        classifys.append(s_classify)
    db.session.commit()
    return classifys


@manage.route('/manage/classifys', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_classifys():

    add_classify = AddClassifyForm()
    del_classify_id = ManageWithIDs(Classify)
    if request.args.get('do') == 'del':
        if del_classify_id.validate_on_submit():
            list(map(db.session.delete, del_classify_id.datas))
            db.session.commit()
            return redirect(url_for('manage.manage_classifys'))
    if request.args.get('do') == 'add':
        if add_classify.validate_on_submit():
            classify = Classify()
            classify.classify = add_classify.classify.data
            db.session.add(classify)
            db.session.commit()
            return redirect(url_for('manage.manage_classifys'))

    classifys = Classify.query.filter_by().all()
    return render_template('manage/classifys.html',
                           add_classify=add_classify,
                           del_classify_id=del_classify_id, classifys=classifys)


@manage.route('/manage/users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    del_user_id = ManageWithIDs(User)
    if request.args.get('do') == 'del':
        if del_user_id.validate_on_submit():
            list(map(db.session.delete, del_user_id.datas))
            db.session.commit()
        return redirect(url_for('manage.manage_users'))
    return render_template('manage/users.html', users=users, id_list=del_user_id)


@manage.route('/manage/posts', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_posts():
    del_post_id = ManageWithIDs(Post)
    if request.args.get('do') == 'del':
        if del_post_id.validate_on_submit():
            list(map(db.session.delete, del_post_id.datas))
            db.session.commit()
            return redirect(url_for('manage.manage_posts'))
    posts = Post.query.all()
    return render_template('manage/posts.html', posts=posts, id_list=del_post_id)
