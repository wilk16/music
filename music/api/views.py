from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    CreateAPIView,
)

from music.models import Band
from music.api.serializers import (
    BandListSerializer,
    BandDetailSerializer,
    BandCreateUpdateSerializer,
)

class BandCreateAPIView(CreateAPIView):
    #queryset = Band.objects.all()
    serializer_class = BandCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)
        serializer.save(modify_by=self.request.user)


class BandListAPIView(ListAPIView):
    queryset = Band.objects.all()
    serializer_class = BandListSerializer

class BandDetailAPIView(RetrieveAPIView):
    queryset = Band.objects.all()
    serializer_class = BandDetailSerializer
    lookup_field = 'slug'

class BandUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Band.objects.all()
    serializer_class = BandCreateUpdateSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(modify_by=self.request.user)


class BandDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Band.objects.all()
    serializer_class = BandDetailSerializer
    lookup_field = 'slug'

