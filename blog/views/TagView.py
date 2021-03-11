
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.generics import ListAPIView

from blog.models.Tag import Tag

from blog.serializers.TagSerializer import TagModelSerializer


class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer

