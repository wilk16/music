from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^band/(?P<pk>[0-9]+)/$', views.BandView.as_view(), name='band'),
        url(r'^record/(?P<pk>[0-9]+)/$', views.RecordView.as_view(),
            name='record'),
        url(r'^genre/(?P<pk>[0-9]+)/$', views.GenreView.as_view(), name='genre'),
        url(r'^label/(?P<pk>[0-9]+)/$', views.LabelView.as_view(), name='label'),
        url(r'^userPanel/$', views.UserPanelView.as_view(), name='userPanel'),

        url(r'^band_list/(?P<page_nb>[0-9]+)/$', views.BandListView.as_view(),
            name='band_list'),

        url(r'^label_list/(?P<page_nb>[0-9]+)/$', views.LabelListView.as_view(),
            name='label_list'),
        url(r'^genre_list/(?P<page_nb>[0-9]+)/$', views.GenreListView.as_view(),
            name='genre_list'),
        url(r'^record_list/(?P<page_nb>[0-9]+)/$', views.RecordListView.as_view(),
            name='record_list'),
        url(r'^contact/$', views.contact, name='contact'),
]
