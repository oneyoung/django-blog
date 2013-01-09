from django.conf.urls import patterns, include, url
from blog import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/', 'blog.views.admin_login'),
    url(r'^admin/edit/', views.EditView.as_view()),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>.+)/',
        views.BlogView.as_view(), name='blog_view'),
    # Examples:
    # url(r'^$', 'blogsite.views.home', name='home'),
    # url(r'^blogsite/', include('blogsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
