from flask_wtf import FlaskForm
from wtforms import (BooleanField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import Email, Length, Required, ValidationError

from ..models import Role, User


class EditProfileForm(FlaskForm):
    name = StringField('真实名字', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    confirmed = BooleanField('邮箱验证')
    role = SelectField('权限', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            ValidationError("这个邮箱已经注册过了")

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            ValidationError("这个用户名已经注册过了已经注册过了")


class PostForm(FlaskForm):
    title = StringField('标题', validators=[Required(), Length(1, 256)])
    body = TextAreaField('正文')
    submit = SubmitField('提交')
