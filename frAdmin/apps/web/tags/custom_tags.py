from django import template
from django.shortcuts import render
from django.urls import reverse

register = template.Library()


@register.simple_tag
def breadcrumb_item(title, url, is_active=False, icon_class='', **kwargs):
    if is_active:
        return '<li class="active"><i class="' + icon_class + ' position-left"></i>' + title + "</li>"
    else:
        return '<li><a href="' + reverse(url,kwargs=kwargs) + '"><i class="' + icon_class + ' position-left"></i>'\
               + title + "</a></li>"


@register.filter(name='addclass')
def addclass(value, arg):
    css_classes = value.field.widget.attrs.get('class', None).split(' ')
    if css_classes and arg not in css_classes:
        css_classes = '%s %s' % (css_classes, arg)
    return value.as_widget(attrs={'class': css_classes})


@register.simple_tag
def status_tag(status):
    if status:
        return '<div class="text-muted"><span class="label bg-success heading-text">Enabled</span></div>'
    else:
        return '<div class="text-muted"><span class="label bg-warning heading-text">Disable</span></div>'
