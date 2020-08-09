from django.urls import path
from . import views


def get_frontend_urls():
    return [path("plot", views.first_plot)]
