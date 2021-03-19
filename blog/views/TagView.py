
from rest_framework.generics import ListAPIView

from blog.models.Tag import Tag

from blog.serializers.TagSerializer import TagModelSerializer


class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer

