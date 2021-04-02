
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter

from blog.models.Language import Language

from blog.serializers.LanguageSerializer import LanguageModelSerializer


class LanguageListView(ListAPIView):
    serializer_class = LanguageModelSerializer
    pagination_class = None
    filter_backends = (OrderingFilter, )
    ordering_fields = ['name']

    def get_queryset(self):
        queryset = Language.objects.all()

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset


