from django.urls import path
import auth_system.views as views

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("log-out/", views.CustomLogoutView.as_view(), name="log-out"),
    path("register/", views.RegisterView.as_view(), name="register"),
]

app_name = "auth_system"