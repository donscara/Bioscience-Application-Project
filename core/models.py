from django.db import models


class Base(models.Model):

    objects = models.Manager()

    class Meta:
        abstract = True
        default_manager_name = "objects"
