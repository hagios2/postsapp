from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    # path('posts/<int:pk>/update/', views.update_post, name='post_update'),
    # path('posts/<int:pk>/delete/', views.delete_post, name='post_delete'),
]