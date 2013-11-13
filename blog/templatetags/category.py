# -*- coding: utf8 -*-
from django import template
from blog.models import Category

register = template.Library()


@register.assignment_tag
def category_list():
    return [{'name': c.name, 'slug': c.slug}
            for c in Category.objects.all().order_by('rank')]
