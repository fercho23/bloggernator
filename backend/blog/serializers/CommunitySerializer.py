
from rest_framework import serializers

from blog.models.Community import Community

from blog.serializers.UserSerializer import UserModelSerializer


class CommunityModelSerializer(serializers.ModelSerializer):
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


class CommunityCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = (
            'name',
            'detail',
        )

