from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.get_posts, name="posts"),
    path("posts_no_dep/", views.get_posts_no_dependency, name="posts_no_dep"),
    path("posts_listv/", views.BlogPostListView.as_view(), name="posts_listv")
]
