from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('comentarios_usuario/', views.comentarios_usuario, name='comentarios_usuario'),
    #path('ratings_usuario/', views.ratings_usuario, name='ratings_usuario'),
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]