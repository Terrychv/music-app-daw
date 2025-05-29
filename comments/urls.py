from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]