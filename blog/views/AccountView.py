
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from blog.serializers.AccountSerializer import LoginSerializer, SignupSerializer
from blog.serializers.UserSerializer import UserModelSerializer


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj, token = serializer.save()

            response = {}
            response['user'] = UserModelSerializer(obj).data
            response['token'] = token

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request, **kwargs):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
            invalidate_token = Token.objects.filter(key=token, user=request.user)
            invalidate_token.delete()

            return Response({'detail': _('Logged out')}, status=status.HTTP_200_OK)
        except:
            return Response({'error': [_('Token does not exist!')]}, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    model = get_user_model()
    permission_classes = (AllowAny, )
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = SignupSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj, token = serializer.save()

            response = {}
            response['user'] = UserModelSerializer(obj).data
            response['token'] = token

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)