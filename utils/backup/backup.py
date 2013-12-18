#!/usr/bin/env python
import os

target = ['/www/django-blog/db',
    '/www/django-blog/media']
bak_dst = '/home/oneyoung/Dropbox/backup'

if not os.path.isdir(bak_dst):
    os.system('mkdir -p %s' % bak_dst)

for t in target:
    os.system("rsync -vaz --delete %s %s" % (t, bak_dst))
