from django.urls import path
from django.urls import re_path
from . import views

from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path('', views.index),
    re_path(r'^favicon\.ico$', favicon_view),
]