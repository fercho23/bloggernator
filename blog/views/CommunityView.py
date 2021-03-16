
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from blog.models.Community import Community

from blog.serializers.CommunitySerializer import CommunityModelSerializer, CommunityCreateUpdateSerializer


class CommunityCreateView(CreateAPIView):
    serializer_class = CommunityCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommunityDeleteView(DestroyAPIView):
    queryset = Community.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise ValidationError({'detail': _('Only the community owner can perform this action.')})

        if instance.members.count() > 0:
            raise ValidationError({'detail': _('Only the communities without members can be deleted.')})

        instance.delete()


class CommunityListView(ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunityModelSerializer


class CommunityUpdateView(UpdateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunityCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.owner:
            raise ValidationError({'detail': _('Only the community owner can perform this action.')})

        serializer.save()
