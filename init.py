#!/usr/bin/python2
import os


def check_moudle(name, package=None):
    if not package:
        package = name
    try:
        __import__(name)
    except ImportError:
        print ("%s not found" % name)
        print ("run: `easy_install -U %s` to install" % package)
        exit(1)

check_moudle('django_evolution')
check_moudle('markdown')

project_dir = os.path.dirname(os.path.abspath(__file__))

config = '''
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

SECRET_KEY = 'YOUR_SECRET_KEY_HERE'
'''
config_path = os.path.join(project_dir, "blogsite/config.py")
if not os.path.exists(config_path):
    f = open(config_path, 'w')
    f.write(config)
    f.close()

db_path = os.path.join(project_dir, "db")
if not os.path.exists(db_path):
    os.mkdir(db_path)
