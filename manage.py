#!/usr/bin/env python2
import os
import sys

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    if project_dir not in sys.path:
        sys.path.append(project_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogsite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
