from django.urls import path
from . import views

urlpatterns = [
    path("rec", views.record, name="record"),
    path("save", views.save, name="save"),
    path("student", views.Student_reg, name="student"),
    path("login", views.my_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    
]