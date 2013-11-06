#!/usr/bin/env python
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

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
