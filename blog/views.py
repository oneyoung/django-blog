# -*- coding: utf8 -*-
# Create your views here.
from django import http
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core import exceptions
from django.views.generic import FormView, DetailView, ListView
from models import Blog
from forms import AdminUserForm, BlogForm


class AdminLoginView(FormView):
    form_class = AdminUserForm
    template_name = 'login.html'
    success_url = '/admin/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = AdminUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser and user.is_active:
                    login(request, user)
                    return http.HttpResponseRedirect(self.get_success_url())
        msg = "Invalid username or password, please try again."
        return self.render_to_response({'form': form, 'msg': msg})


def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect('/')


def check_admin(request):
    user = request.user
    if user and user.is_authenticated() and user.is_superuser:
        pass
    else:
        raise exceptions.PermissionDenied


class AdminView(ListView):
    model = Blog
    queryset = Blog.objects.all().order_by("-date_create")
    template_name = 'admin.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        try:
            check_admin(request)
        except exceptions.PermissionDenied:
            return http.HttpResponseRedirect(reverse("admin_login"))

        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class EditView(FormView):
    '''
    kwargs for url
    * new post: /
    * edit existig post: /?pk=primary_key
    '''
    form_class = BlogForm
    template_name = 'edit.html'
    success_url = '/admin/'

    def dispatch(self, request, *args, **kwargs):
        check_admin(request)  # if not admin, will show 403 page
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def _get_blog(pk):
        ''' when pk is 0, return None '''
        try:
            return Blog.objects.get(pk=pk) if pk else Blog()
        except Blog.DoesNotExist:
            raise http.Http404

    def get(self, request, *args, **kwargs):
        pk = int(request.GET.get('pk', 0))
        blog = self._get_blog(pk)
        return self.render_to_response({'blog': blog, 'pk': pk})

    def post(self, request, *args, **kwargs):
        pk = int(request.REQUEST.get('pk', 0))
        blog = self._get_blog(pk)
        form = self.form_class(request.POST, instance=blog)
        if form.is_valid():
            form.save()
        else:
            return self.render_to_response({'blog': blog, 'pk': pk})
        return http.HttpResponseRedirect(self.get_success_url())


class BlogView(DetailView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blog'
    slug_url_kwarg = 'slug'
