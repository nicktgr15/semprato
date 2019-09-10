from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.defaulttags import register
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
                                 logout as auth_logout, get_user_model, update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm


@register.inclusion_tag('login_template_tag.html', takes_context=True)
def show_login_form(context):
    return { "request": context['request'] }