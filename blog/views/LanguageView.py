
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView

from blog.models.Language import Language

from blog.serializers.LanguageSerializer import LanguageModelSerializer


class LanguageListView(APIView):

    def get(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK

        try:
            objects = Language.objects.all()
            serialization = LanguageModelSerializer(objects, many=True).data

            response_data['result'] = True
            response_data['objects'] = serialization
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

