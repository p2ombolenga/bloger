from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config


class GoogleLoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        token = request.data.get('token')

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), config('GOOGLE_CLIENT_ID'))
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first_name,
                    'last_name': last_name
                }
            )

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'is_new_user': created
            })

        except ValueError:
            return Response(
                {'error': 'Invlid Google Token'},
                status=status.HTTP_400_BAD_REQUEST
                )

class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all().prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post_instance = get_object_or_404(Post, id=post_id)
        return serializer.save(user=self.request.user, post=post_instance)
    
class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]