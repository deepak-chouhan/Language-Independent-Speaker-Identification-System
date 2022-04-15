from .models import *
from django import forms
from django.forms import ModelForm


class Studentform(forms.ModelForm):
    class Meta:
        model=Student
        fields='__all__'
