# coding: utf-8

import django
from django.conf import settings
import app_config

# NOTICE : call django setting first to allow define models
settings.configure(DATABASES=app_config.DB_IMPORTER_DATABASES, INSTALLED_APPS=['importer'])
# Calling django.setup() is required for “standalone” Django usage
django.setup()