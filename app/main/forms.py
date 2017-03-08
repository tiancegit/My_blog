# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, ValidationError
from wtforms.validators import DataRequired, length
from ..moudle import Post


class PostForm(FlaskForm):
    title = StringField(u'标题', [DataRequired(), length(max=255)])
    short_title = StringField(u'英文短标题', [DataRequired(), length(max=255)])
    body = TextAreaField(u'文章内容', [DataRequired()])

    def __init__(self):
        super(PostForm, self).__init__()

    def validate_short_title(self, field):
        # 检查短标题是否唯一
        if Post.query.filter_by(short_title=field.data).first():
            raise ValidationError(u'英文短标题已经存在,请更改英文短标题.')