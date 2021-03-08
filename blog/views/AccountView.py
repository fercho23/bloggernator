
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

from blog.serializers.AccountSerializer import SignupSerializer
from blog.serializers.UserSerializer import UserSerializer


class SignupView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK
        serializer = SignupSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            obj = User.objects.create_user(
                email=data['email'],
                username=data['username'],
                password=data['password'],
            )

            obj_serializer = UserSerializer(obj, context={'request': request})

            response_data['result'] = True
            # response_data['object'] = JSONRenderer().render(obj_serializer.data)
            response_data['object'] = obj_serializer.data
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

