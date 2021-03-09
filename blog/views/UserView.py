
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from blog.models.User import User

from blog.serializers.UserSerializer import UserModelSerializer, UserUpdateSerializer


class UserDetailView(APIView):

    def get(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK
        serializer = None

        try:
            pk = kwargs.get('pk')
            obj = User.objects.filter(uuid=pk).first()
            if not obj:
                raise ObjectDoesNotExist(_("User do not exist."))

            serialization = UserModelSerializer(obj).data

            response_data['result'] = True
            response_data['object'] = serialization
        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            response_data['error'] = True

            if isinstance(e, ValidationError):
                status = HTTP_422_UNPROCESSABLE_ENTITY
                response_data['validation_errors'] = e.get_full_details() if not serializer or not serializer.errors else serializer.errors
            else:
                if isinstance(e, ObjectDoesNotExist):
                    status = HTTP_404_NOT_FOUND
                response_data['message'] = str(e)

        return Response(response_data, status=status)


class UserUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def put(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK
        serializer = None

        try:
            pk = kwargs.get('pk', '')

            if request.user.uuid != pk:
                raise ValidationError({'pk': _("User is not correct.")})

            obj_to_serialize = request.user
            # obj_to_serialize = User.objects.filter(uuid=pk).first()
            # if not obj_to_serialize:
            #     raise ObjectDoesNotExist(_("User do not exist."))

            serializer = UserUpdateSerializer(obj_to_serialize, data=request.data)
            serializer.is_valid(raise_exception=True)

            obj = serializer.save()
            serialization = UserModelSerializer(obj).data

            response_data['result'] = True
            response_data['object'] = serialization
        except Exception as e:
            status = HTTP_400_BAD_REQUEST
            response_data['error'] = True

            if isinstance(e, ValidationError):
                status = HTTP_422_UNPROCESSABLE_ENTITY
                response_data['validation_errors'] = e.get_full_details() if not serializer or not serializer.errors else serializer.errors
            else:
                if isinstance(e, ObjectDoesNotExist):
                    status = HTTP_404_NOT_FOUND
                response_data['message'] = str(e)

        return Response(response_data, status=status)
