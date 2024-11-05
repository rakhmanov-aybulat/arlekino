from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('solve/', views.solve_captcha, name='solve_captcha'),
]

