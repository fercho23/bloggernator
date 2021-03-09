
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from blog.models.User import User


class UserModelSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'username',
            'photo_url',
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            photo_url = obj.photo.url
            return photo_url
            return request.build_absolute_uri(photo_url)
        return ''

        # request = self.context.get('request', None)
        # if request and obj.photo:
        #     photo_url = obj.photo.url
        #     return request.build_absolute_uri(photo_url)
        # return ''


class UserUpdateSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )

    class Meta:
        model = User
        fields = [
            'username',
            'photo',
        ]

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