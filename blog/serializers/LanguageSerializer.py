
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from blog.models.Language import Language


class LanguageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = (
            'uuid',
            'name',
            'slug',
        )


