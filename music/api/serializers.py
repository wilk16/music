from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField)

from music.models import Band, Record

class BandListSerializer(ModelSerializer):
    class Meta:
        model = Band
        fields = ('name',
                  'origin')

class BandDetailSerializer(ModelSerializer):
    class Meta:
        model = Band
        fields = ('id',
                  'name',
                 'origin',
                 'record_set')
        read_only_fields = ('id', 'record_set',)

class BandCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Band
        fields = ('name', 'origin',)

