from django.db import models
from django.utils import encoding


class Comment(models.Model):
    pass


class Blog(models.Model):
    slug = models.SlugField(max_length=255, editable=False, unique_for_month='date_create')
    title = models.CharField(max_length=255)
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now=True)
    body_html = models.TextField()
    body_raw = models.TextField(blank=True, null=True)
    RAW_FORMAT_CHOICES = (
        ('html', 'HTML Format'),
        ('md', 'Markdown'),
    )
    raw_format = models.CharField(max_length=10, choices=RAW_FORMAT_CHOICES, default='html')
    #comment = models.OneToOneField(Comment)

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        if not self.slug:  # new object here
            self.slug = self.title
        if self.raw_format == 'md':
            self.body_html = self.body_raw
        self.full_clean()
        models.Model.save(self, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('blog_view', (), {
            'year': self.date_create.strftime('%Y'),
            'month': self.date_create.strftime('%m'),
            'slug': self.slug})
