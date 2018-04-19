from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Login(FlaskForm):
    email = StringField(validators=[DataRequired('邮箱不能为空'),
                                    Length(1, 64, "邮箱输入有误"), Email("邮箱输入有误")],
                        render_kw={"placeholder": "邮箱(帐号)"})
    password = PasswordField(validators=[DataRequired('密码不能为空')],
                             render_kw={"placeholder": "密码"})
    remember_me = BooleanField("下次自动登陆")
    submit = SubmitField("登陆")


class Register(FlaskForm):
    email = StringField(validators=[DataRequired('邮箱不能为空'),
                                    Length(1, 64, "邮箱输入有误"), Email("邮箱输入有误")],
                        render_kw={"placeholder": "邮箱(帐号)"})
    user_name = StringField(validators=[DataRequired('用户名不能为空')],
                            render_kw={"placeholder": "用户名"})
    password_first = PasswordField(validators=[DataRequired('密码不能为空')],
                                   render_kw={"placeholder": "密码"})
    password_second = PasswordField(validators=[EqualTo('password_first',
                                                        '两次输入的密码必须相同')],
                                    render_kw={"placeholder": "再次输入密码"})
    submit = SubmitField("注册")

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError("此邮箱已经注册过了")

    # def validate_user_name(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError("此用户名已经注册过了")
