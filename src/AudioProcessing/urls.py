from django.urls import path
from . import views

urlpatterns = [
    path("", views.record, name="record"),
    path("save", views.save, name="save"),
]