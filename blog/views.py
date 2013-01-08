# -*- coding: utf8 -*-
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
    title = forms.CharField(label='标题', max_length=255)
    body_raw = forms.CharField(label='正文', widget=forms.Textarea)
    raw_format = forms.ChoiceField(label='格式', choices=Blog.RAW_FORMAT_CHOICES)

    class Meta:
        model = Blog
        fields = ('title', 'body_raw', 'raw_format')


class EditView(FormView):
    '''
    kwargs for url
    * new post: /
    * edit existig post: /?pk=primary_key
    '''
    form_class = BlogForm
    template_name = 'edit.html'
    success_url = '/admin/'

    @staticmethod
    def _get_blog(pk):
        ''' when pk is 0, return None '''
        try:
            return Blog.objects.get(pk=pk) if pk else None
        except Blog.DoesNotExist:
            raise http.Http404

    def get(self, request, *args, **kwargs):
        pk = int(request.GET.get('pk', 0))
        blog = self._get_blog(pk)
        form = self.form_class(instance=blog)
        return self.render_to_response({'form': form, 'pk': pk})

    def post(self, request, *args, **kwargs):
        pk = int(request.REQUEST.get('pk', 0))
        blog = self._get_blog(pk)
        form = self.form_class(request.POST, instance=blog)
        if form.is_valid():
            form.save()
        else:
            return self.render_to_response({'form': form, 'pk': pk})
        return http.HttpResponseRedirect(self.get_success_url())
