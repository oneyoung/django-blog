# -*- coding: utf8 -*-
from django import forms
from models import Blog


class AdminUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.widgets.PasswordInput())


class BlogForm(forms.ModelForm):
    title = forms.CharField(label='标题', max_length=255)
    body_raw = forms.CharField(label='正文', widget=forms.Textarea)
    raw_format = forms.ChoiceField(label='格式', choices=Blog.RAW_FORMAT_CHOICES)

    class Meta:
        model = Blog
        fields = ('title', 'body_raw', 'raw_format')
