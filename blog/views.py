# Create your views here.
from django.shortcuts import render
from django import http
from django import forms
from django.contrib.auth import authenticate, login
from models import Blog
from django.views.generic import FormView


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


def get_blog_object(kwargs):
    year = int(kwargs.get('year', 0))
    month = int(kwargs.get('month', 0))
    slug = kwargs.get('slug', '')

    blog = Blog.objects.get(slug=slug, date_create__year=year,
                            date_create__month=month)
    return blog


def blog_view(request, **kwargs):
    try:
        blog = get_blog_object(kwargs)
        return http.HttpResponse("%s" % blog.body_html)
    except:
        raise http.Http404


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog


def post_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return http.HttpResponse("OK")
    f = BlogForm()
    return render(request, 'edit.html', {'form': f})


class EditView(FormView):
    '''
    kwargs for url
    * new post:
        new=True
    * edit existig post:
        year=YYYY
        month=MM
        slug=slug_of_post
    '''
    form_class = BlogForm
    template_name = 'edit.html'

    def get(self, request, *args, **kwargs):
        qdict = request.QueryDict.dict()
        if qdict.get('new', '') == 'True':
            pass
        else:
            pass

    def post(self, request, *args, **kwargs):
        pass
