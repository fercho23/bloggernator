
from rest_framework import serializers

from blog.models.Community import Community


class CommunityModelSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner_uuid = serializers.ReadOnlyField(source='owner.uuid')

    class Meta:
        model = Community
        fields = (
            'uuid',
            'name',
            'slug',
            'detail',
            'created_at',
            'owner_username',
            'owner_uuid',
        )


class CommunityCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = (
            'name',
            'detail',
        )

