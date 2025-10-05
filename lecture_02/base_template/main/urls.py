from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("contact_v2", views.contact_v2, name="contact_v2"),
    path("schedule", views.schedule, name="schedule"),
]
