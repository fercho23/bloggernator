
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from blog.models.Post import Post

from blog.serializers.PostSerializer import PostModelSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all().select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')
    serializer_class = PostModelSerializer


class PostListByLanguageView(ListAPIView):
    serializer_class = PostModelSerializer

    def get_queryset(self):
        """
        This view should return a list of all the post filter by the language
        """
        slug = self.kwargs['slug']
        return Post.objects.filter(language__slug=slug).select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')


class PostListByTagView(ListAPIView):
    serializer_class = PostModelSerializer

    def get_queryset(self):
        """
        This view should return a list of all the post filter by the tag
        """
        slug = self.kwargs['slug']
        return Post.objects.filter(tags__slug=slug).select_related('language', 'community', 'author').prefetch_related('tags', 'contributors')


