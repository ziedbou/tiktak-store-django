from django import template
import json
import os

register = template.Library()

@register.filter
def to_json(obj):
    return json.dumps(obj)


@register.filter
def env(key):
    return os.environ.get(key, None)