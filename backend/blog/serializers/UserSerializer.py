
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserModelCompleteSerializer(serializers.ModelSerializer):
    owns_communities = serializers.SerializerMethodField()
    member_communities = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'uuid',
            'email',
            'username',
            'photo',
            'date_joined',
            'owns_communities',
            'member_communities',
        )

    def get_owns_communities(self, obj):
        from blog.serializers.CommunitySerializer import CommunityModelSerializer

        owns_communities = obj.community_set.all()
        response = CommunityModelSerializer(owns_communities, many=True).data
        return response

    def get_member_communities(self, obj):
        from blog.serializers.CommunitySerializer import CommunityModelSerializer

        member_communities = obj.members.all()
        response = CommunityModelSerializer(member_communities, many=True).data
        return response


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'uuid',
            # 'email',
            'username',
            'photo',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'photo',
        )

    def validate(self, data):
        image = data.get('photo', None)
        if image:
            if image.size > (512 * 1024):
                raise serializers.ValidationError(_('The image is too large, the maximum weight allowed is 512KB and the size sent is {} KB'.format(round (image.size / 1024))))

        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()

        return instance