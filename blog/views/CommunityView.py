
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from blog.models.Community import Community

from blog.serializers.CommunitySerializer import CommunityModelSerializer


class CommunityListView(ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunityModelSerializer


