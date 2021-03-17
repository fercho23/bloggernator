
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from blog.models.User import User

from blog.serializers.UserSerializer import UserModelSerializer, UserUpdateSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'uuid'


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj:
            raise ValidationError({'detail': _('You can perform this action only on yourself.')})

        serializer.save()
