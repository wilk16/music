from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^band/(?P<pk>[0-9]+)/$', views.BandView.as_view(), name='band'),
        url(r'^record/(?P<pk>[0-9]+)/$', views.RecordView.as_view(),
            name='record'),
        url(r'^userPanel/$', views.UserPanelView.as_view(), name='userPanel'),
        url(r'^band_list/$', views.BandListView.as_view(), name='band_list'),
        url(r'^label_list/$', views.BandListView.as_view(), name='label_list'),
        url(r'^genre_list/$', views.BandListView.as_view(), name='genre_list'),
        url(r'^record_list/$', views.BandListView.as_view(), name='record_list'),
]
