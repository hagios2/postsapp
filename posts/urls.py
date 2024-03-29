from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.list_posts, name='homepage'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/update/', views.update_post, name='post_update'),
    path('posts/<int:pk>/delete/', views.delete_post, name='post_delete'),
]