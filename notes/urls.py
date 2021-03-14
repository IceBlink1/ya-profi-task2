from django.conf.urls import url

from notes import views

urlpatterns = [
    url(r'^api/notes$', views.notes),
    url(r'^api/notes/(?P<pk>[0-9]+)$', views.note_detail),
]
