from django.db import models


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

    @models.permalink
    def get_absolute_url(self):
        return ('blog_view', (), {
            'year': self.date_create.strftime('%Y'),
            'month': self.date_create.strftime('%m'),
            'title': self.title})
