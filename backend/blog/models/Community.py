
import uuid

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Community(Group):
    uuid = models.CharField(_('uuid'), editable=False, blank=True, max_length=254, default=uuid.uuid4, unique=True, db_index=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('owner'))
    slug = models.SlugField(_('slug'), max_length=255, unique=True, blank=True)
    detail = models.CharField(_('detail'), max_length=180, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('members'), blank=True, related_name='members')

    created_at = models.DateTimeField(_('created at'), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('community')
        verbose_name_plural = _('communities')
        ordering = ('name',)
        permissions = [
            ('community_owner', 'Community owner'),
            ('community_member', 'Community member'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Community, self).save(*args, **kwargs)