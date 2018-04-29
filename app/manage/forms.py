from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import (BooleanField, FieldList, FormField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import Email, Length, Regexp, Required, ValidationError

from..models import Role, User, Tag, Classify


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
            raise ValidationError("这个邮箱已经注册过了")

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError("这个用户名已经注册过了已经注册过了")


class PostForm(FlaskForm):
    title = StringField('标题', validators=[Required('标题不能为空'), Length(1, 256)])
    # body = TextAreaField('正文')
    body = PageDownField("正文", validators=[Required('正文不能为空')])
    tags = StringField('标签名称', validators=[Length(0, 64), Regexp(
        '^[\u4e00-\u9fa5\w]*[,\u4e00-\u9fa5\w]*$', message='标签格式出现问题')])
    classifys = StringField('分类名称', validators=[Length(0, 64), Regexp(
        '^[\u4e00-\u9fa5\w]*[,\u4e00-\u9fa5\w]*$', message='分类格式出现问题')])
    submit = SubmitField('提交')


class AddTagForm(FlaskForm):
    tag = StringField('标签名称', validators=[Required(message='标签不能为空'),
                                          Length(
                                              1, 64, message='输入过长或过短(1-64)'),
                                          Regexp('^[\u4e00-\u9fa5\w]+$',
                                                 message='不能包含除汉字和英文以外的其他字符')])
    submit = SubmitField('提交')

    def validate_tag(self, field):
        if Tag.query.filter_by(tag=field.data).first():
            raise ValidationError("已经有了相同的标签插入失败")


class DelTagForm(FlaskForm):
    tags = StringField('标签名称',
                       validators=[
                           Required(message='标签为空'),
                           Regexp('^[\u4e00-\u9fa5\w]+[,\u4e00-\u9fa5\w]*$',
                                  message='删除标签失败')])
    submit = SubmitField('提交')

    def validate_tags(self, field):
        if not all(map(self.select_sql, field.data.split(','))):
            raise ValidationError("想要删除不存在的标签")

    def select_sql(self, tag):
        tmp = Tag.query.filter_by(tag=tag).first()
        if tmp:
            return tmp
        return None


class AddClassifyForm(FlaskForm):
    classify = StringField('分类名称', validators=[Required(message='分类不能为空'),
                                               Length(
        1, 64, message='输入过长或过短(1-64)'),
        Regexp('^[\u4e00-\u9fa5\w]+$',
               message='不能包含除汉字和英文以外的其他字符')])
    submit = SubmitField('提交')

    def validate_classify(self, field):
        if Classify.query.filter_by(classify=field.data).first():
            raise ValidationError("已经有了相同的分类插入失败")


class DelClassifyForm(FlaskForm):
    classifys = StringField('分类名称',
                            validators=[
                                Required(message='输入分类为空'),
                                Regexp('^[\u4e00-\u9fa5\w]+[,\u4e00-\u9fa5\w]*$',
                                       message='删除分类失败')])
    submit = SubmitField('提交')

    def validate_classifys(self, field):
        if not all(map(self.select_sql, field.data.split(','))):
            raise ValidationError("想要删除不存在的分类")

    def select_sql(self, classify):
        tmp = Classify.query.filter_by(classify=classify).first()
        if tmp:
            return tmp
        return None
