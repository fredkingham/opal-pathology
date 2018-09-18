import json
from django import template
from pathology.pathology_categories import PathologyCategory

register = template.Library()


def construct_context(context, category_name):
    ctx["pathology_category"] = PathologyCategory.get(category_name)
    return ctx

@register.inclusion_tag('pathology/templatetags/pathology_form.html', takes_context=True)
def pathology_form(context, category_name):
    return construct_context(context, category_name)

@register.inclusion_tag('pathology/templatetags/pathology_detail.html', takes_context=True)
def pathology_detail(context, category_name):
    return construct_context(context, category_name)

@register.inclusion_tag('pathology/templatetags/pathology_display.html', takes_context=True)
def pathology_display(context, category_name):
    return construct_context(context, category_name)