
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from blog.models.Post import Post

from blog.serializers.UserSerializer import UserModelSerializer
from blog.serializers.LanguageSerializer import LanguageModelSerializer
from blog.serializers.CommunitySerializer import CommunityModelSerializer
from blog.serializers.TagSerializer import TagModelSerializer


class PostModelSerializer(serializers.ModelSerializer):
    author = UserModelSerializer()
    community = CommunityModelSerializer()
    language = LanguageModelSerializer()
    tags = TagModelSerializer(many=True)
    contributors = UserModelSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'uuid',
            'title',
            'slug',
            'body',
            'abstract',

            'author',
            'community',
            'language',
            'tags',
            'contributors',
        )


