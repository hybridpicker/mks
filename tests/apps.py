"""
Django App Configuration für Tests
"""

from django.apps import AppConfig

class TestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tests'
    verbose_name = 'MKS Test Suite'
