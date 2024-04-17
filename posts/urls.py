from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('auth/user/posts/', views.get_posts_for_auth_user, name='auth_user_posts'),
    path('post/for/', views.AuthUserPostsList.as_view(), name='post_for_auth_user'),
]