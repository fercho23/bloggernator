

from rest_framework.generics import ListAPIView

from blog.models.Language import Language

from blog.serializers.LanguageSerializer import LanguageModelSerializer


class LanguageListView(ListAPIView):
    queryset = Language.objects
    serializer_class = LanguageModelSerializer
    pagination_class = None


