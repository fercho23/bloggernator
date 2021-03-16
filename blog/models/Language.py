
import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    uuid = models.CharField(_('uuid'), editable=False, blank=True, max_length=254, default=uuid.uuid4, unique=True, db_index=True)

    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Language, self).save(*args, **kwargs)