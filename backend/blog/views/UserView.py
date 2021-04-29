
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from blog.serializers.UserSerializer import UserModelCompleteSerializer, UserModelSerializer, UserUpdateSerializer

User = get_user_model()


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def perform_destroy(self, serializer):
        obj = self.get_object()

        if not self.request.user.is_superuser and self.request.user != obj:
            raise ValidationError({'detail': _('You can perform this action only on yourself.')})

        serializer.delete()


class UserListView(ListAPIView):
    serializer_class = UserModelSerializer
    filter_backends = (OrderingFilter, )
    ordering_fields = ['username']

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True).all()

        query_params = self.request.query_params

        username = query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username__icontains=username)

        not_in_username = query_params.get('not_in_username')
        if not_in_username is not None:
            not_in_username = query_params.getlist('not_in_username')
        if not_in_username is None:
            not_in_username = query_params.get('not_in_username[]')
            if not_in_username is not None:
                not_in_username = query_params.getlist('not_in_username[]')

        if not_in_username is not None:
            queryset = queryset.exclude(username__in=not_in_username)

        return queryset


class UserReadView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelCompleteSerializer
    lookup_field = 'username'

    def get_object(self):
        pk = self.kwargs.get(self.lookup_field)

        if pk == 'current':
            return self.request.user

        return super(UserReadView, self).get_object()


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
