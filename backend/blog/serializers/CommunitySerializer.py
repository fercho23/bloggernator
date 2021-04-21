
from rest_framework import serializers

from blog.models.Community import Community



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

    class Meta:
        model = Community
        fields = (
            'name',
            'detail',
        )

