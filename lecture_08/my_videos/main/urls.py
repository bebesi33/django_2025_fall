from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("videos/", views.show_videos, name="videos"),
    path("add_new_video/", views.add_video, name="add_video"),
    # path("videos/<int:id>/", views.video_detail_view, name="video_detail"),
    # path("videos/delete/<int:id>/", views.video_delete_view, name="video_delete"),
    path("video_list_view", views.VideoListView.as_view(), name="video_list_view"),
    path("add_video_class/", views.VideoCreateView.as_view(), name="add_video_class"),
    path("videos/<int:id>/", views.VideoUpdateView.as_view(), name="video_detail"),
    path("videos/delete/<int:id>/", views.VideoDeleteView.as_view(), name="video_delete"),
]
