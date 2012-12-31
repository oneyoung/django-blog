from django.db import models

class Comment(models.Model):
    pass


class Blog(models.Model):
    url = models.URLField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now=True)
    body_html = models.TextField()
    body_md = models.TextField()
    comment = models.OneToOneField(Comment)

    def __unicode__(self):
        return self.title
