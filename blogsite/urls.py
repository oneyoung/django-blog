from django.conf.urls import patterns, url
from blog import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.BlogListView.as_view(), name='home'),
    url(r'^login/$', views.AdminLoginView.as_view(), name='admin_login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^admin/$', views.AdminView.as_view(), name='admin'),
    url(r'^admin/edit/$', views.EditView.as_view(), name='edit'),
    url(r'^admin/settings/$', views.SettingsView.as_view(), name='settings'),
    url(r'^admin/uploadimg/$', views.UploadImageView.as_view(), name='uploadimg'),
    url(r'^admin/imginfo/$', views.ImageInfoView.as_view(), name='imginfo'),
    url(r'^archive/tag/(?P<tag>.+)/$',
        views.BlogListView.as_view(), name='tag'),
    url(r'^archive/date/(?P<year>\d{4})(?P<month>\d{2})/$',
        views.BlogListView.as_view(), name='date'),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>.+)/$',
        views.BlogView.as_view(), name='blog'),
    url(r'^feed/$', views.RSSFeed(), name='feed'),
    # Examples:
    # url(r'^$', 'blogsite.views.home', name='home'),
    # url(r'^blogsite/', include('blogsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

from blogsite import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )
