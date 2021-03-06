# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, ValidationError, SubmitField
from wtforms.validators import DataRequired, length, Email, Regexp, Optional
from ..models import Post


class PostForm(FlaskForm):
    title = StringField(u'标题', validators=[DataRequired(message=u'这个字段是必填项'), length(max=255)])
    short_title = StringField(u'英文短标题', validators=[DataRequired(message=u'这个字段是必填项'), length(max=255)])
    tags = StringField(u"标签", validators=[DataRequired(message=u'这个字段是必填项')])
    category = SelectField(u'选择分类', choices=[('技术', '技术'), ('杂谈', '杂谈')], validators=[DataRequired(message=u'这个字段是必选项')])
    body = TextAreaField(u'文章内容', validators=[DataRequired()])
    submit = SubmitField(u'提交')

    def __init__(self):
        super(PostForm, self).__init__()

    def validate_short_title(self, field):
        # 检查短标题是否唯一
        if Post.query.filter_by(short_title=field.data).first():
            raise ValidationError(u'英文短标题已经存在,请更改英文短标题.')


class EditPostForm(FlaskForm):
    title = StringField(u'标题', validators=[DataRequired(), length(max=255)])
    short_title = StringField(u'英文短标题', validators=[DataRequired(), length(max=255)])
    body = TextAreaField(u'文章内容', validators=[DataRequired()])

    def __init__(self):
        super(EditPostForm, self).__init__()


class CommentForm(FlaskForm):
    author_name = StringField('', validators=[DataRequired(), length(1, 64)])
    author_email = StringField('', validators=[Optional(), length(1, 64), Email(message='这不是一个有效的邮箱地址')])
    author_website = StringField('', validators=[Optional(), length(1, 64),
                                                    Regexp(r'''(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|
                                                    [a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+
                                                    \)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,
                                                    <>?«»“”‘’]))''', 0, u'这不是一个有效的网址')])
    content_body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField(u'提交')

