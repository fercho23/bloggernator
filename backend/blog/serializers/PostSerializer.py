
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from blog.models.Community import Community
from blog.models.Language import Language
from blog.models.Post import Post
from blog.models.Tag import Tag

from blog.serializers.UserSerializer import UserModelSerializer
from blog.serializers.LanguageSerializer import LanguageModelSerializer
from blog.serializers.CommunitySerializer import CommunityModelSerializer
from blog.serializers.TagSerializer import TagModelSerializer

User = get_user_model()


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


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    community = serializers.SlugRelatedField(
        many=False,
        queryset=Community.objects.select_related('owner').prefetch_related('members').all(),
        slug_field='slug',
        # slug_field='uuid',
     )

    language = serializers.SlugRelatedField(
        many=False,
        queryset=Language.objects.all(),
        slug_field='slug',
        # slug_field='uuid',
     )

    # tags = serializers.SlugRelatedField(
    #     many=True,
    #     queryset=Tag.objects.all(),
    #     slug_field='uuid',
    #     allow_null=False,
    #  )

    # contributors = serializers.SlugRelatedField(
    #     many=True,
    #     queryset=User.objects.all(),
    #     slug_field='uuid',
    #     allow_null=False,
    #  )

    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='slug',
     )

    contributors = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='username',
     )

    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'abstract',

            'community',
            'language',
            'tags',
            'contributors',
        )
