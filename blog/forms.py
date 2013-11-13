# -*- coding: utf8 -*-
import json
from django import forms
from models import Blog, Category


class AdminUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.widgets.PasswordInput())


class BlogForm(forms.Form):
    title = forms.CharField(label='标题', max_length=255)
    body_raw = forms.CharField(label='正文', widget=forms.Textarea)
    raw_format = forms.ChoiceField(label='格式', choices=Blog.RAW_FORMAT_CHOICES)
    tags = forms.CharField(required=False, max_length=1024)
    status = forms.CharField(max_length=100)
    category = forms.CharField()

    def saveto(self, blog):
        blog.title = self.cleaned_data['title']
        blog.body_raw = self.cleaned_data['body_raw']
        blog.raw_format = self.cleaned_data['raw_format']
        blog.status = self.cleaned_data['status']

        tags_str = self.cleaned_data['tags']
        tags = json.loads(tags_str, encoding="utf8")
        blog.update_tags(tags)

        category = self.cleaned_data['category']
        blog.category = Category.objects.get(slug=category)

        blog.save()
