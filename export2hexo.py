import os
import sys

project_dir = os.path.dirname(os.path.abspath(__file__))

# load virtualenv if necessary
virtualenv = os.path.join(project_dir, 'virtualenv')
activate_this = os.path.join(virtualenv, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    execfile(activate_this, dict(__file__=activate_this))

if __name__ == "__main__":
    if project_dir not in sys.path:
        sys.path.append(project_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogsite.settings")


from blog.models import Blog

SAVED_DIR = '/tmp/exports'
front_matter_templ = '''layout: post
title: "%(title)s"
date: %(date)s
updated: %(update)s
tags: [%(tags)s]
categories: %(categories)s
---
%(content)s
'''


def save2md(content, filename):
    saved_path = os.path.join(SAVED_DIR, filename + '.md')
    fp = open(saved_path, 'w')
    fp.write(content.encode('utf8'))
    fp.close()


if not os.path.exists(SAVED_DIR):
    os.mkdir(SAVED_DIR)

print '###Exported posts will be saved in %s ###' % SAVED_DIR

for post in filter(lambda p: p.raw_format == 'md', Blog.objects.all()):
    print 'converting: ' + post.title
    meta = {
        'title': post.title,
        'tags': ','.join([t.name for t in post.tags.all()]),
        'date': post.date_create.strftime("%Y/%m/%d %H:%M:%S"),
        'update': post.date_modify.strftime("%Y/%m/%d %H:%M:%S"),
        'categories': post.category.name if post.category else '',
        'content': '\n'.join(post.body_raw.splitlines()),
    }
    content = front_matter_templ % meta
    filename = str(post.id) + '-' + post.slug
    save2md(content, filename)
