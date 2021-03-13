
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    uuid = models.CharField(_('uuid'), editable=False, blank=True, max_length=254, default=uuid.uuid4, unique=True, db_index=True)

    title = models.CharField(_('title'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    body = models.TextField(_('body'))
    abstract = models.CharField(_('abstract'), max_length=250)

    # author = models.ForeignKey('User', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField('Tag', verbose_name=_('tags'), blank=True, related_name='tags')
    # contributors = models.ManyToManyField('User', verbose_name=_('contributors'), blank=True, related_name='contributors')

    is_public = models.BooleanField(_('public'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-created_at',)
        permissions = [
            ('post_owner', 'Post owner'),
            ('post_contributor', 'Post contributor'),
        ]

    def __str__(self):
        return self.title
