from django.db import models
from django.utils import encoding
import re
import urllib


class Comment(models.Model):
    pass


class Blog(models.Model):
    title = models.CharField(max_length=255, unique_for_month='date_create')
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now=True)
    body_html = models.TextField()
    body_md = models.TextField(blank=True, null=True)
    #comment = models.OneToOneField(Comment)

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        self.full_clean()
        models.Model.save(self, **kwargs)


class BlogManage(models.Manager):
    @classmethod
    def get_path_by_blog(cls, blog):
        if isinstance(blog, Blog) is False:
            raise AttributeError("not an instance of Blog")
        time = blog.date_create
        prefix = "%s/%s/" % (time.year, time.month)
        path = prefix + encoding.iri_to_uri(blog.title)
        return path

    @classmethod
    def get_blog_by_path(cls, path):
        try:
            m = re.match('(\d+)/(\d+)/(.*)', path).groups()
            year = int(m[0])
            month = int(m[1])
            title = encoding.smart_unicode(urllib.unquote(m[2]))
            blog = Blog.objects.get(title=title,
                                    date_create__year=year, date_create__month=month)
            return blog
        except:
            return None
