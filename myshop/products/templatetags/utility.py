from django import template

register = template.Library()

@register.simple_tag
def get_model_name(obj):
    return obj.__class__.__name__

@register.simple_tag
def get_value_by_key(source, key):
    if isinstance(source, dict):
        return source.get(key)
    return source

@register.filter(name='not_null')
def get_not_empty(source):
    return (itm for itm in source if itm)
