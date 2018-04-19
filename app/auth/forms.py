from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class Login(FlaskForm):
    email = StringField(validators=[DataRequired('邮箱不能为空'),
                                    Length(1, 64, "邮箱输入有误"), Email("邮箱输入有误")],
                        render_kw={"placeholder": "邮箱(帐号)"})
    password = PasswordField(validators=[DataRequired('密码不能为空')],
                             render_kw={"placeholder": "密码"})
    remember_me = BooleanField("下次自动登陆")
    submit = SubmitField("登陆")
