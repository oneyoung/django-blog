# Create your views here.
from django.shortcuts import render
from django import http
from django import forms
from django.contrib.auth import authenticate, login
from django.utils import encoding
import urllib
from models import Blog


class AdminUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.widgets.PasswordInput())


def admin_login(request):
    msg = ""
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser and user.is_active:
                    login(request, user)
                    return http.HttpResponseRedirect('/admin/')
        msg = "Invalid username or password, please try again."
    f = AdminUserForm()
    return render(request, 'login.html', {'form': f, 'msg': msg})


def blog_view(request, **kwargs):
    year = int(kwargs.get('year', 0))
    month = int(kwargs.get('month', 0))
    title = encoding.smart_unicode(urllib.unquote(kwargs.get('title', '')))

    try:
        blog = Blog.objects.get(title=title, date_create__year=year,
                                date_create__month=month)
        return http.HttpResponse("%s" % blog.body_html)
    except:
        raise http.Http404
