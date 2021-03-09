
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from blog.models.Tag import Tag


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'uuid',
            'name',
            'slug',
        ]


