# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.filter
def multiply(a, b):
    return a * b


@register.filter
def divide(a, b):
    return float(a) / float(b)

@register.filter
def intiger(a):
    return int(a)
