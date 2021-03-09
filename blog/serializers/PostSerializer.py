
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from blog.models.Post import Post


class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'uuid',
            'title',
            'slug',
            'body',
            'abstract',
        ]


