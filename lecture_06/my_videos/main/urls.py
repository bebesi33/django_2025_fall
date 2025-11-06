from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("videos/", views.show_videos, name="videos"),
    path("add_new_video/", views.add_video, name="add_video"),
]
