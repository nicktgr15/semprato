from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    # context = {'name': 'nikos'}
    return redirect(reverse("article_manager:home"))