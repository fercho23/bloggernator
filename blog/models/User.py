
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


from blog.managers.UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    uuid = models.CharField(_('uuid'), editable=False, blank=True, max_length=254, default=uuid.uuid4, unique=True, db_index=True)

    email = models.EmailField(_('email'), max_length=254, unique=True)
    username = models.CharField(_('username'), max_length=254, unique=True)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    photo = models.ImageField(upload_to='users', blank=True, null=True, verbose_name=_('photo'))

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
       return '{}'.format(self.email)

    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse('user.update', args=[str(self.id)])

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
