# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from . import auth
from .forms import LoginForm, RegistrationForm
from ..moudle import User, db
from flask_login import login_user, login_required, logout_user, current_user
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名/密码错误', 'info')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    # 退出函数
    logout_user()
    flash(u'你已经退出了', 'info')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # 注册函数,发送确认邮件,包含令牌
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user, token=token)
        flash(u'确认邮件已经发送至你的邮箱.', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # 邮件确认链接.
    if current_user.confirmed:
        # 若是已经确认的,定向去首页
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'你已成功确认账户', 'info')
    else:
        flash(u'确认链接错误或已过期.请重新发送!')
    return redirect(url_for('main.index'))


@auth.before_app_request()
def before_request():
    # 1:用户已经登录.2:用户的账户未确认.3:请求的端点不在认证蓝本中(auth)
    if current_user.is_authenticated \
            and not current_user.cofirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

