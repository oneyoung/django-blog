# -*- coding: utf8 -*-
from django import template
from django.core import exceptions
from blog.models import Setting

register = template.Library()
OPTIONS = (
    #(name, help_msg),
)


@register.simple_tag
def get_setting(name):
    try:
        item = Setting.objects.get(name=name)
        value = item.value
    except exceptions.ObjectDoesNotExist:
        value = ""

    return value
