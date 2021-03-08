
from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from blog.models.User import User


class SignupSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'password_confirmation',
            'photo',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({'password': _('Password fields didn\'t match.')})

        image = None
        if 'photo' in attrs:
            image = attrs['photo']

        if image:
            if image.size > (512 * 1024):
                raise serializers.ValidationError(_('The image is too large, the maximum weight allowed is 512KB and the size sent is {} KB'.format(round (image.size / 1024))))

        return attrs
