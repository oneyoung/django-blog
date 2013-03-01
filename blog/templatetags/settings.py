# -*- coding: utf8 -*-
from django import template
from django.core import exceptions
from blog.models import Setting

register = template.Library()
OPTIONS = [
    # ('name', 'help_msg'),
    ('blog_name', 'The name of your blog'),
    ('blog_desc', 'Brief description of your blog'),
    ('google_analystics_id', 'Google Analystics Tracking ID'),
    ('disqus_shortname', 'Website shortname registered in Disqus'),
]


@register.simple_tag
def get_setting(name):
    try:
        item = Setting.objects.get(name=name)
        value = item.value
    except exceptions.ObjectDoesNotExist:
        value = ""

    return value


@register.simple_tag
def get_options():
    result = []
    for name, hint in OPTIONS:
        result += {
            'name': name,
            'help': hint,
            'value': Setting.objects.get_or_create(name=name).value
        }
    return result
