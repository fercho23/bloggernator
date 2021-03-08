
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
        request = self.context.get('request', None)
        if request and obj.photo:
            photo_url = obj.photo.url
            return request.build_absolute_uri(photo_url)
        return ''