from flask import flash, redirect, render_template, request, url_for
from flask_login import (UserMixin, current_user, login_required, login_user,
                         logout_user)
from werkzeug.security import generate_password_hash

from . import auth
from .. import db
from ..email import send_email
from ..models import User
from .forms import Login, Register


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        email = form.email.data
        user_name = form.user_name.data
        password = form.password_first.data
        user = User(email=email, username=user_name,
                    password=password)
        db.session.add(user)
        db.session.commit()
        token = user.genrate_confirmation_tonken()
        send_email(user.email, "确认你的帐号", 'auth/email/confirm',
                   user=user, token=token)
        flash('确认邮件已经发出,请在一小时之内确认')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效的帐户名和密码')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('你将要注销登陆')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('你已经确认了你的帐号')
    else:
        flash('链接已经失效了')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    else:
        return render_template("auth/unconfirmed.html")


@auth.route('/confirm')
@login_required
def resend_confirmation():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    token = current_user.genrate_confirmation_tonken()
    send_email(current_user.email, "确认你的帐号", 'auth/email/confirm',
               user=current_user, token=token)
    flash('确认邮件已经发出,请在一小时之内确认')
    return redirect(url_for('main.index'))
