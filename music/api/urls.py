from django.conf.urls import url
from django.conf import settings
from music.api.views import (
    BandListAPIView,
    BandDetailAPIView,
    BandUpdateAPIView,
    BandDeleteAPIView,
    BandCreateAPIView,
)
from django.conf.urls.static import static

urlpatterns = [
        url(r'^band/$', BandListAPIView.as_view(), name='band'),
        url(r'^band/create/$', BandCreateAPIView.as_view(),
            name='band_create'),
        url(r'^band/(?P<slug>[-\w]+)/$', BandDetailAPIView.as_view(),
            name='band_detail'),
        url(r'^band/(?P<slug>[-\w]+)/update/$', BandUpdateAPIView.as_view(),
            name='band_update'),
        url(r'^band/(?P<slug>[-\w]+)/delete/$', BandDeleteAPIView.as_view(),
            name='band_delete'),
]
