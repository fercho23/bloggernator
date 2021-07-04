
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

from rest_framework import serializers

from blog.models.Community import Community

User = get_user_model()


class CommunityModelCompleteSerializer(serializers.ModelSerializer):
    from blog.serializers.UserSerializer import UserModelSerializer
    from blog.serializers.PostSerializer import PostModelBasicSerializer

    owner = UserModelSerializer()
    members = UserModelSerializer(many=True)
    # last_posts = PostModelBasicSerializer(many=True)
    last_posts = serializers.SerializerMethodField()


    class Meta:
        model = Community
        fields = (
            'uuid',
            'name',
            'slug',
            'detail',
            'photo',
            'created_at',
            'owner',
            'members',

            'last_posts',
        )

    def get_last_posts(self, obj):
        from blog.serializers.PostSerializer import PostModelBasicSerializer
        objects = obj.post_set.all()[:10]
        return PostModelBasicSerializer(objects, many=True).data


class CommunityModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = (
            'uuid',
            'name',
            'slug',
            'detail',
            'photo',
            'created_at',
        )


class CommunityCreateUpdateSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='username',
    )
    photo = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
    )

    class Meta:
        model = Community
        fields = (
            'name',
            'detail',
            'members',
            'photo',
        )

    def validate(self, data):
        image = data.get('photo', None)
        if image:
            if image.size > (512 * 1024):
                raise serializers.ValidationError(_('The image is too large, the maximum weight allowed is 512KB and the size sent is {} KB'.format(round(image.size / 1024))))

        return data