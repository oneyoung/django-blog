from django.db import models
from datetime import datetime


class Setting(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=1024, blank=True, null=True)

    def __unicode__(self):
        return self.name


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
        ('album', 'Photo Album'),
    )
    raw_format = models.CharField(max_length=10, choices=RAW_FORMAT_CHOICES, default='html')
    active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    STATUS_CHOICES = (
        ('public', 'Post'),
        ('draft', 'Save as Draft'),
        ('delete', 'Delete!'),
        ('private', 'Private Only!'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='public')

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        def alloc_slug(title):
            slug = title.replace(' ', '-')
            if Blog.objects.filter(slug=slug):  # found slug conflict
                slug = slug + datetime.now().strftime("_%y%m%d-%H%M%S")
            return slug

        def raw2html(raw, type):
            def md2html(raw):
                import markdown
                md = markdown.Markdown(extensions=['fenced_code'])
                return md.convert(raw)

            def album2html(raw):
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(raw)
                desc = soup.find(id='album-desc')

                images = soup.find(id='album-images')
                for imgtag in images.find_all(['img']):
                    idx = imgtag.get('data-id')
                    img = Image.objects.get(idx=idx)
                    imgtag['src'] = img.thumb_url
                    imgtag['alt'] = img.desc if img.desc else ''
                    imgtag['data-src'] = img.img_url

                divcover = soup.new_tag('div', id='album-cover')
                coverid = images.get('data-cover')
                coverimg = images.find(lambda tag: tag.get('data-id') == coverid)
                import copy
                divcover.append(copy.deepcopy(coverimg))

                return '\n'.join(map(lambda div: div.prettify(),
                                     [divcover, desc, images]))

            if type == 'md':
                html = md2html(raw)
            elif type == 'html':
                html = raw
            elif type == 'album':
                html = album2html(raw)
            return html

        if not self.id:  # new object here
            self.slug = alloc_slug(self.title)
        self.body_html = raw2html(self.body_raw, self.raw_format)

        self.full_clean()
        models.Model.save(self, **kwargs)

    def update_tags(self, tag_list):
        if not self.id:  # new here, need to save before update m2m fields
            self.save()
        tags_new = set(
            map(lambda n: Tag.objects.get_or_create(name=n)[0], tag_list))
        tags_old = set(self.tags.all())
        for tag in tags_old - tags_new:
            self.tags.remove(tag)
        for tag in tags_new - tags_old:
            self.tags.add(tag)

    @models.permalink
    def get_absolute_url(self):
        return ('blog', (), {
            'year': self.date_create.strftime('%Y'),
            'month': self.date_create.strftime('%m'),
            'slug': self.slug})


class Image(models.Model):
    idx = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='image/', blank=True, null=True)
    _img_url = models.URLField(blank=True, null=True)
    thumb = models.ImageField(upload_to='image/thumb/', blank=True, null=True)
    _thumb_url = models.URLField(blank=True, null=True)

    desc = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=15, default='')
    active = models.BooleanField(default=True)

    blogs = models.ForeignKey(Blog, blank=True, null=True)

    def _get_img_url(self):
        return self._img_url if self._img_url else self.img.url

    def _set_img_url(self, url):
        self._img_url = url

    img_url = property(_get_img_url, _set_img_url)

    def _get_thumb_url(self):
        if self._thumb_url:
            url = self._thumb_url
        elif self.thumb:
            url = self.thumb.url
        else:
            url = self.img_url
        return url

    def _set_thumb_url(self, url):
        self._thumb_url = url

    thumb_url = property(_get_thumb_url, _set_thumb_url)
