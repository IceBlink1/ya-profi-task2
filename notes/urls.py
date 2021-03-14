from django.conf.urls import url

from notes import views

urlpatterns = [
    url(r'^notes$', views.notes),
    url(r'^notes/(?P<pk>[0-9]+)$', views.note_detail),
]
