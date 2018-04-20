from flask import render_template
from . import main
from flask import redirect, url_for


@main.app_errorhandler(404)
def page_not_founf(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
