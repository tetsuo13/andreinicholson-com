#!/usr/bin/env python

import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../django')))
sys.path.insert(0, project_path)
sys.path.insert(0, os.path.abspath(os.path.join(project_path, 'vendor')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method='threaded', daemonize='false')
