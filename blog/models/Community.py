
import uuid

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class Community(Group):
    uuid = models.CharField(_('uuid'), editable=False, blank=True, max_length=254, default=uuid.uuid4, unique=True, db_index=True)

    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    detail = models.CharField(_('detail'), max_length=180, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')
        ordering = ('-created_at',)
        permissions = [
            ('community_owner', 'Community owner'),
            ('community_member', 'Community member'),
        ]