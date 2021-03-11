
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView

from blog.models.Post import Post

from blog.serializers.PostSerializer import PostModelSerializer


class PostListView(APIView):

    def get(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK
        serializer = None

        try:
            objects = Post.objects.all()
            serialization = PostModelSerializer(objects, many=True).data

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


class PostListByLanguageView(APIView):

    def get(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK
        serializer = None

        try:
            slug = kwargs.get('slug', '')

            objects = Post.objects.filter(language__slug=slug).all()
            serialization = PostModelSerializer(objects, many=True).data

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


class PostListByTagView(APIView):

    def get(self, request, *args, **kwargs):
        response_data = {}
        status = HTTP_200_OK
        serializer = None

        try:
            slug = kwargs.get('slug', '')

            objects = Post.objects.filter(tags__slug=slug).all()
            serialization = PostModelSerializer(objects, many=True).data

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

