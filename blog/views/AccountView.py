
from PIL import Image

# from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


from rest_framework.exceptions import ValidationError
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView

from blog.models.User import User

from blog.serializers.AccountSerializer import LoginSerializer, SignupSerializer
from blog.serializers.UserSerializer import UserModelSerializer


class SignupView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK
        serializer = SignupSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            obj, token = serializer.save()
            obj_serialized = UserModelSerializer(obj, context={'request': request}).data

            response_data['result'] = True
            response_data['object'] = obj_serialized
            response_data['access_token'] = token
        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            response_data['error'] = True

            if isinstance(e, ValidationError):
                status = HTTP_422_UNPROCESSABLE_ENTITY
                response_data['validation_errors'] = e.get_full_details() if not serializer.errors else serializer.errors
            else:
                if isinstance(e, ObjectDoesNotExist):
                    status = HTTP_404_NOT_FOUND
                response_data['message'] = str(e)

        return Response(response_data, status=status)


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK
        serializer = LoginSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            obj, token = serializer.save()
            obj_serialized = UserModelSerializer(obj, context={'request': request}).data

            response_data['result'] = True
            response_data['object'] = obj_serialized
            response_data['access_token'] = token
        except Exception as e:

            status = HTTP_400_BAD_REQUEST
            response_data['error'] = True

            if isinstance(e, ValidationError):
                status = HTTP_422_UNPROCESSABLE_ENTITY
                response_data['validation_errors'] = e.get_full_details() if not serializer.errors else serializer.errors
            else:
                if isinstance(e, ObjectDoesNotExist):
                    status = HTTP_404_NOT_FOUND
                response_data['message'] = str(e)

        return Response(response_data, status=status)

