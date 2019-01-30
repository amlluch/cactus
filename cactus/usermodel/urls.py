from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name="register"),
    path('token/', views.Token.as_view()),
    path('token/refresh/', views.RefreshToken.as_view()),
    path('token/revoke/', views.RevokeToken.as_view()),
]