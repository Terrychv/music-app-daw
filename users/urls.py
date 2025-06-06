from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit_username/', views.edit_username, name='edit_username'),
    path('change-avatar/', views.change_avatar, name='change_avatar'),
]
