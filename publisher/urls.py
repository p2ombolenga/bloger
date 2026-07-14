from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', views.CommentListCreateAPIView.as_view(), name='comment-list'),
    path('posts/<int:post_id>/comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view(), name='coment-detail'),
]