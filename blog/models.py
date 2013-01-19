from django.db import models
from datetime import datetime


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Blog(models.Model):
    slug = models.SlugField(max_length=255, editable=False, unique=True)
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
    active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        if not self.id:  # new object here
            slug = self.title.replace(' ', '-')
            if Blog.objects.filter(slug=slug):  # found slug conflict
                slug = slug + datetime.now().strftime("_%y%m%d-%H%M%S")
            self.slug = slug

        if self.raw_format == 'md':
            import markdown
            md = markdown.Markdown(extensions=['fenced_code'])
            self.body_html = md.convert(self.body_raw)
        elif self.raw_format == 'html':
            self.body_html = self.body_raw

        self.full_clean()
        models.Model.save(self, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('blog_view', (), {
            'year': self.date_create.strftime('%Y'),
            'month': self.date_create.strftime('%m'),
            'slug': self.slug})
