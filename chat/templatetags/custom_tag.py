from django import template
from django.contrib.auth import get_user_model

register = template.Library()


@register.simple_tag
def get_user_model_by_username(username):
    return get_user_model().objects.filter(username=username).first()
