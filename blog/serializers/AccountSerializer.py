
from django.contrib.auth import password_validation, authenticate
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from blog.models.User import User


class LoginSerializer(serializers.Serializer):

    # Campos que vamos a requerir
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    # Primero validamos los datos
    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


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

    def validate(self, data):
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError({'password': _('Password fields didn\'t match.')})
        password_validation.validate_password(password)

        image = data.get('photo', None)
        if image:
            if image.size > (512 * 1024):
                raise serializers.ValidationError(_('The image is too large, the maximum weight allowed is 512KB and the size sent is {} KB'.format(round (image.size / 1024))))

        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        # token, created = Token.objects.get_or_create(user=self.context['user'])
        token, created = Token.objects.get_or_create(user=user)
        return user, token.key