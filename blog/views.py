# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate


class AdminUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.widgets.PasswordInput())


def admin_login(request):
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    return HttpResponseRedirect('/admin/')
    f = AdminUserForm()
    return render(request, 'login.html', {'form': f})
