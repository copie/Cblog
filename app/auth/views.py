from flask import flash, render_template

from . import auth
from .forms import Login


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        return redirect(request.args.get('next') or url_for('main.index'))

    flash('无效的帐户名和密码')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    return "注册"
