
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from blog.models.User import User
from blog.serializers.UserSerializer import UserModelCompleteSerializer, UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def perform_destroy(self, serializer):
        obj = self.get_object()

        if not self.request.user.is_superuser and self.request.user != obj:
            raise ValidationError({'detail': _('You can perform this action only on yourself.')})

        serializer.delete()


class UserReadView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelCompleteSerializer
    lookup_field = 'username'


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def perform_update(self, serializer):
        obj = self.get_object()

        if not self.request.user.is_superuser and self.request.user != obj:
            raise ValidationError({'detail': _('You can perform this action only on yourself.')})

        serializer.save()
