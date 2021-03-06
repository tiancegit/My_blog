# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import length, Email, EqualTo, Regexp, DataRequired
from ..models import User


class LoginForm(FlaskForm):
    # 登录的表单
    email = StringField(u'邮箱', validators=[DataRequired(), length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), length(1, 64), Email(message='这不是一个有效的邮箱地址')])
    username = StringField(u'用户名', validators=[DataRequired(), length(1, 64),
                                               Regexp('^[A-Za-z\u4e00-\u9fa5][A-Za-z0-9\u4e00-\u9fa5._]*$', 0,
                                                      u'用户名必须以中文或字母开头,只能包含中文，字母，数字，点或下划线')])
    password = PasswordField(u'密码', validators=[DataRequired(), EqualTo('password2', message=u'两次输入的密码不一致')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册,更换邮箱或者找回密码.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被占用,请更换用户名.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码', validators=[DataRequired()])
    password = PasswordField(u'新密码',  validators=[DataRequired(), EqualTo('password2', message=u'两次密码输入不一致')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'修改密码')


class PasswordRestRequestForm(FlaskForm):
    email = StringField(u'注册邮箱', validators=[DataRequired(), length(1, 64), Email()])
    submit = SubmitField(u'找回密码')


class PasswordRestForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), length(1, 64), Email()])
    password = PasswordField(u'新密码', validators=[DataRequired(), EqualTo('password2', message=u'两次密码输入不一致!')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'修改密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮箱地址错误')

