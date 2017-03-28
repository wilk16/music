from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^band/(?P<pk>[0-9]+)/$', views.BandView.as_view(), name='band'),
        url(r'^record/(?P<pk>[0-9]+)/$', views.RecordView.as_view(),
            name='record'),
        url(r'^userPanel/$', views.UserPanelView.as_view(), name='userPanel'),
]
