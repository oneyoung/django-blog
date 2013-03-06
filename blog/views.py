# -*- coding: utf8 -*-
# Create your views here.
from django import http
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, resolve
#from django.core import exceptions
from django.views.generic import FormView, DetailView, ListView
from django.contrib.syndication.views import Feed
from models import Blog, Tag, Setting
from forms import AdminUserForm, BlogForm


class AdminLoginView(FormView):
    form_class = AdminUserForm
    template_name = 'admin/login.html'
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


def check_permission(cls):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user and user.is_authenticated() and user.is_superuser:
            return super(self.__class__, self).dispatch(request, *args, **kwargs)
        else:
            return http.HttpResponseRedirect(reverse("admin_login"))

    cls.dispatch = dispatch
    return cls


@check_permission
class AdminView(ListView):
    model = Blog
    queryset = Blog.objects.exclude(status='delete').order_by("-date_create")
    template_name = 'admin/admin.html'
    paginate_by = 10


@check_permission
class EditView(FormView):
    '''
    kwargs for url
    * new post: /
    * edit existig post: /?pk=primary_key
    '''
    form_class = BlogForm
    template_name = 'admin/edit.html'
    success_url = '/admin/'

    @staticmethod
    def _get_blog(pk):
        ''' when pk is 0, return empty Blog() '''
        try:
            return Blog.objects.get(pk=pk) if pk else Blog()
        except Blog.DoesNotExist:
            raise http.Http404

    def get(self, request, *args, **kwargs):
        pk = int(request.GET.get('pk', 0))
        blog = self._get_blog(pk)
        return self.render_to_response({'blog': blog, 'pk': pk, 'tags': Tag.objects.all()})

    def post(self, request, *args, **kwargs):
        pk = int(request.REQUEST.get('pk', 0))
        blog = self._get_blog(pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            form.saveto(blog)
        else:
            return self.render_to_response({'blog': blog, 'pk': pk, 'tags': Tag.objects.all()})
        return http.HttpResponseRedirect(self.get_success_url())


@check_permission
class SettingsView(FormView):
    form_class = Setting
    template_name = 'admin/settings.html'
    success_url = '/admin/'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        for name, value in request.POST.items():
            setting, created = Setting.objects.get_or_create(name=name)
            setting.value = value
            setting.save()
        return http.HttpResponseRedirect(self.get_success_url())


class BlogView(DetailView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blog'
    slug_url_kwarg = 'slug'


class BlogListView(ListView):
    template_name = 'index.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        if not self.queryset:
            try:
                path = self.request.path
                view_name = resolve(path).url_name
                context = dict(self.kwargs)
                context['path'] = path
                context['view_name'] = view_name
                self._context = context
                if view_name == 'home':
                    queryset = Blog.objects.all()
                elif view_name == 'tag':
                    name = self.kwargs.get('tag')
                    tag = Tag.objects.get(name=name)
                    queryset = tag.blog_set.all()
                elif view_name == 'date':
                    year = int(self.kwargs.get('year', 0))
                    month = int(self.kwargs.get('month', 0))
                    queryset = Blog.objects.filter(date_create__year=year,
                                                   date_create__month=month)
                else:
                    raise LookupError
            except:
                raise http.Http404
            self.queryset = queryset.filter(status='public').order_by("-date_create")
        return self.queryset

    def get_context_data(self, **kwargs):
        context = kwargs
        context.update(self._context)
        return super(self.__class__, self).get_context_data(**context)


class RSSFeed(Feed):
    def link(self):
        return reverse('feed')

    def items(self):
        queryset = Blog.objects.all()
        return queryset.filter(status='public').order_by("-date_create")[0:8]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body_html

    def item_link(self, item):
        return item.get_absolute_url()
