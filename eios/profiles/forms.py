#encoding: UTF-8
import os
from django import forms
from django.contrib.auth.models import User
from .models import Application, UserDetail


class DeptQueryForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['dept']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']


class UserDetailForm(forms.ModelForm):

    class Meta:
        model = UserDetail
        exclude = ['user', 'languages']


class UserDetailShortForm(forms.ModelForm):

    class Meta:
        model = UserDetail
        exclude = ['user', 'is_professor', 'languages']