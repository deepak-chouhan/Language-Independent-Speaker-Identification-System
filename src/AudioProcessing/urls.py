from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_view, name="login"),
    path("rec", views.record, name="record"),
    path("save", views.save, name="save"),
    path("student", views.Student_reg, name="student"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("logout", views.logout_view, name="logout"),
]