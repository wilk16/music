from django.conf.urls import url
from django.conf import settings
from music.api.views import *
"""
(
    BandListAPIView,
    BandDetailAPIView,
    BandUpdateAPIView,
    BandDeleteAPIView,
    BandCreateAPIView,
)
"""
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

        url(r'^label/$', LabelListAPIView.as_view(), name='label'),
        url(r'^label/create/$', LabelCreateAPIView.as_view(),
            name='label_create'),
        url(r'^label/(?P<slug>[-\w]+)/$', LabelDetailAPIView.as_view(),
            name='label_detail'),
        url(r'^label/(?P<slug>[-\w]+)/update/$', LabelUpdateAPIView.as_view(),
            name='label_update'),
        url(r'^label/(?P<slug>[-\w]+)/delete/$', LabelDeleteAPIView.as_view(),
            name='label_delete'),

        url(r'^genre/$', GenreListAPIView.as_view(), name='genre'),
        url(r'^genre/create/$', GenreCreateAPIView.as_view(),
            name='genre_create'),
        url(r'^genre/(?P<slug>[-\w]+)/$', GenreDetailAPIView.as_view(),
            name='genre_detail'),
        url(r'^genre/(?P<slug>[-\w]+)/update/$', GenreUpdateAPIView.as_view(),
            name='genre_update'),
        url(r'^genre/(?P<slug>[-\w]+)/delete/$', GenreDeleteAPIView.as_view(),
            name='genre_delete'),

]
