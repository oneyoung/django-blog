# Create your views here.
from django.shortcuts import render
from django.http import HttpResonpseRedirect
from django import forms
from django.contrib.auth import authenticate


class AdminUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


def admin_login(request):
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = AdminUserForm.cleaned_date
