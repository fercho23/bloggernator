
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'uuid',
            'email',
            'username',
            'photo_url',
        )

    def get_photo_url(self, obj):
        if obj.photo:
            photo_url = obj.photo.url
            return photo_url
        return ''


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