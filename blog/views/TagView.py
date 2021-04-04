
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter

from blog.models.Tag import Tag

from blog.serializers.TagSerializer import TagModelSerializer


class TagListView(ListAPIView):
    serializer_class = TagModelSerializer
    filter_backends = (OrderingFilter, )
    ordering_fields = ['name']

    def get_queryset(self):
        queryset = Tag.objects.all()

        query_params = self.request.query_params

        name = query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset
