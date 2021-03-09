
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from blog.models.Category import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'uuid',
            'name',
            'slug',
        ]


