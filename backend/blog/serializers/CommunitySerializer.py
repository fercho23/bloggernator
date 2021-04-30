
from django.contrib.auth import get_user_model

from rest_framework import serializers

from blog.models.Community import Community

User = get_user_model()


class CommunityModelCompleteSerializer(serializers.ModelSerializer):
    from blog.serializers.UserSerializer import UserModelSerializer

    owner = UserModelSerializer()
    members = UserModelSerializer(many=True)

    class Meta:
        model = Community
        fields = (
            'uuid',
            'name',
            'slug',
            'detail',
            'created_at',
            'owner',
            'members',
        )


class CommunityModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = (
            'uuid',
            'name',
            'slug',
            'detail',
            'created_at',
        )


class CommunityCreateUpdateSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='username',
     )

    class Meta:
        model = Community
        fields = (
            'name',
            'detail',
            'members',
        )
