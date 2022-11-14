from django.db import models
from apps.models import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=20, null=False, default="")
    email = models.CharField(max_length=100, null=False, default="")
    password = models.CharField(max_length=255, null=False, default="")

    class Meta:
        db_table = "user"
        abstract = False
        managed = True
