from django.db import models
from datetime import datetime
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Setting(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=1024, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    rank = models.IntegerField(blank=True, null=True, default=0)

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
    category = models.ForeignKey(Category, blank=True, null=True)

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

                images_orig = soup.find(id='album-images')
                coverid = images_orig.get('data-cover')
                images = soup.new_tag('div', id='album-images')
                for imgtag in images_orig.find_all(['img']):
                    try:
                        idx = imgtag.get('data-id')
                        img = Image.objects.get(idx=idx)
                        self.image_set.add(img)
                        imgtag['src'] = img.thumb_url
                        imgtag['alt'] = img.desc if img.desc else ''
                        imgtag['data-src'] = img.img_url
                        images.append(imgtag)
                    except:  # ignore illegal img
                        pass

                divcover = soup.new_tag('div', id='album-cover')
                try:
                    coverimg = images.find(lambda tag: tag.get('data-id') == coverid)
                    import copy
                    divcover.append(copy.deepcopy(coverimg))
                except:
                    pass

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

    STATUS_CHOICES = (
        ('created', 'obj has been just created'),
        ('uploaded', 'image has been uploaded'),
        ('updated', 'related blog has been updated'),
        ('invalid', 'url is invalid'),
    )
    status = models.CharField(max_length=15, default='created')
    active = models.BooleanField(default=True)

    blog = models.ForeignKey(Blog, blank=True, null=True)

    def __unicode__(self):
        return str(self.idx)

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


# According django doc, delete() may not be called when
# doing objects.delete(), so need to register a hanlder
# to delete related files before Image.delete()
@receiver(pre_delete, sender=Image)
def image_delete_handler(sender, **kwargs):
    image = kwargs.get('instance')
    for f in [image.img, image.thumb]:
        if f:
            f.delete(save=True)


# admin hook
from django.contrib import admin

admin.site.register(Setting)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Image)
