#!/usr/bin/env python

import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../django')))
sys.path.insert(0, project_path)
sys.path.insert(0, os.path.abspath(os.path.join(project_path, 'vendor')))

# Questionable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../../.local/lib/python2.6/site-packages/flup-1.0.2-py2.6.egg')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method='threaded', daemonize='false')
