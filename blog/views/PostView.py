
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from blog.models.Post import Post

from blog.serializers.PostSerializer import PostModelSerializer


class PostListView(ListAPIView):
    serializer_class = PostModelSerializer
    filter_backends = (OrderingFilter, )
    ordering_fields = ['title']

    def get_queryset(self):
        queryset = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors').all()

        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset.filter(title__icontains=title)

        tags = self.request.query_params.get('tags')
        if tags is not None:
            queryset = queryset.filter(tags__slug=tags)

        language = self.request.query_params.get('language')
        if language is not None:
            queryset = queryset.filter(language__slug=language)

        return queryset
