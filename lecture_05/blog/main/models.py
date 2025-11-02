from django import forms
from django.db import models
from datetime import datetime


class BaseModelWithDateStamp(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    version_number = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.version_number += 1
        super().save(*args, **kwargs)


class BlogPost(BaseModelWithDateStamp):
    title = models.CharField(
        max_length=200,
        primary_key=True,
        help_text="A blog post címe",
        verbose_name="Cím!!"
    )
    content = models.TextField(
        help_text="A blog post tartalma",
        verbose_name="Tartalom!!"
    )

    def __str__(self):
        return self.title
