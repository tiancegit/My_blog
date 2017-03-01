# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, length


class PostForm(FlaskForm):
    title = StringField(u'标题', [DataRequired(), length(max=255)])
    body = TextAreaField(u'文章内容', [DataRequired()])

    def __init__(self):
        super(PostForm, self).__init__()
