from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # path("registration/", views.registration, name="registration"),
    path("registration/", views.RegisterView.as_view(), name="registration"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("sign_out/", views.sign_out, name="sign_out")
    # path("sign_out/", LogoutView.as_view(template_name="logout.html"), name="sign_out")
]