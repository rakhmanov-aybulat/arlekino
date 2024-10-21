from django.urls import include, path


urlpatterns = [
    path("", include("captcha_solver_app.urls")),
]

