from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='api-register'),
    path('login/', views.user_login, name='api-login'),
    path('logout/', views.user_logout, name='api-logout'),
    path('edit-profile/', views.edit_profile, name='api-edit-profile'),
    path('change-password/', views.change_password, name='api-change-password'),
]
