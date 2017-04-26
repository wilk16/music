from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    CreateAPIView,
)

from music.models import Band, Label, Genre
from music.api.serializers import *



class BandCreateAPIView(CreateAPIView):
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



class LabelCreateAPIView(CreateAPIView):
    serializer_class = LabelCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)
        serializer.save(modify_by=self.request.user)

class LabelListAPIView(ListAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelListSerializer

class LabelDetailAPIView(RetrieveAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelDetailSerializer
    lookup_field = 'slug'

class LabelUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelCreateUpdateSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(modify_by=self.request.user)

class LabelDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelDetailSerializer
    lookup_field = 'slug'


class GenreCreateAPIView(CreateAPIView):
    serializer_class = GenreCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)
        serializer.save(modify_by=self.request.user)

class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer

class GenreDetailAPIView(RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializer
    lookup_field = 'slug'

class GenreUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreCreateUpdateSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(modify_by=self.request.user)

class GenreDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializer
    lookup_field = 'slug'

