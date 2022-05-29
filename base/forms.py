from dataclasses import field
from django import forms 
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task 
        exclude = ["user"]


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username" , "first_name" , "last_name" , "email"]