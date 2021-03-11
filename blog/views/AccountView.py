
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# from rest_framework.generics import CreateAPIView
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from blog.serializers.AccountSerializer import LoginSerializer, SignupSerializer
from blog.serializers.UserSerializer import UserModelSerializer


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

            return Response(response, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj, token = serializer.save()

            response = {}
            response['user'] = UserModelSerializer(obj).data
            response['token'] = token

            return Response(response, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request, **kwargs):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
            invalidate_token = Token.objects.filter(key=token, user=request.user)
            invalidate_token.delete()

            return Response({ detail: "Logged out"}, status=HTTP_200_OK)
        except:
            return Response({"error": ["Token does not exist!"]}, status=HTTP_400_BAD_REQUEST)