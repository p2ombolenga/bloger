from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListCreateAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
]