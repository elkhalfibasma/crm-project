from __future__ import absolute_import, unicode_literals
# Cela permet d'importer les tâches lorsque Django démarre
from .celery_app import app as celery_app

__all__ = ('celery_app',)
