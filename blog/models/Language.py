
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    uuid = models.CharField(_('uuid'), editable=False, blank=True, max_length=254, default=uuid.uuid4, unique=True, db_index=True)

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ('name',)

    def __str__(self):
        return self.name