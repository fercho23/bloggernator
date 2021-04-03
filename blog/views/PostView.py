
# from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

# from blog.models.Community import Community
# from blog.models.Language import Language
from blog.models.Post import Post
# from blog.models.Tag import Tag
from blog.serializers.PostSerializer import PostCreateUpdateSerializer, PostModelSerializer

# User = get_user_model()


class PostCreateView(CreateAPIView):
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        community = serializer.validated_data.get('community')

        if user != community.owner and user not in community.members.all():
            raise ValidationError({'detail': _('Only post owner or member of {} can perform this action.').format(community.name)})

        serializer.save(author=self.request.user)


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


class PostReadView(RetrieveAPIView):
    queryset = Post.objects.select_related('language', 'community', 'author').prefetch_related('tags', 'contributors').all()
    serializer_class = PostModelSerializer
    lookup_field = 'uuid'


class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def perform_update(self, serializer):
        obj = self.get_object()
        user = self.request.user

        if user != obj.author and user not in obj.contributors.all():
            raise ValidationError({'detail': _('Only post author or contributors can perform this action.')})

        community = serializer.validated_data.get('community')
        if community is not None and obj.community != community:
            if user != community.owner and user not in community.members.all():
                raise ValidationError({'detail': _('Only post owner or member of {} can perform this action.').format(community.name)})

        serializer.save()