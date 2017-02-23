# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..moudle import User


class LoginForm(FlaskForm):
    # 登录的表单
    email = StringField(u'邮箱', validators=[Required(), length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    email = StringField(u'邮箱', validators=[Required(), length(1, 64), Email()])
    username = StringField(u'用户名', validators=[Required(), length(1, 64),
                                               Regexp('^[A-Za-z\u4e00-\u9fa5][A-Za-z0-9\u4e00-\u9fa5._]*$', 0,
                                                      '用户名必须以中文或字母开头,只能包含中文，字母，数字，点或下划线')])
    password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message='两次输入的密码不一致')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册,更换邮箱或者找回密码.')

    def Validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被占用,请更换用户名.')
