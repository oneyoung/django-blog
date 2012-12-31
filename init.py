#!/usr/bin/python2
import os


project_dir = os.path.dirname(os.path.abspath(__file__))

config = '''
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)

SECRET_KEY = 'YOUR_SECRET_KEY_HERE'
'''
config_path = os.path.join(project_dir, "blogsite/config.py")
if not os.path.exists(config_path):
    f = open(config_path)
    f.write(config)
    f.close()

db_path = os.path.join(project_dir, "db")
if not os.path.exists(db_path):
    os.mkdir(db_path)
