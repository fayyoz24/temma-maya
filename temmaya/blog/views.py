from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, views

from .serializers import BlogPostCreateSerializer, BlogPostGetSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
# Create your views here.
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import BlogPost

class BlogCreateView(CreateAPIView):
    serializer_class = BlogPostCreateSerializer
    queryset = BlogPost.objects.all()
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        # Automatically set the creator to the logged-in user
        serializer.save(creator=self.request.user)


class AllBlogsView(ListAPIView):
    serializer_class = BlogPostGetSerializer

    def get_queryset(self):
        return BlogPost.objects.all()[4:]
class BlogPKView(views.APIView):

    serializer_class = BlogPostGetSerializer

    def get_permissions(self):
        # Allow any user to access the GET method
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        # Require authentication for other methods
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get(self, request, pk):
        data = get_object_or_404(BlogPost, pk=pk)
        data.views_num += 1
        data.save()
        serializer = self.serializer_class(data)
        return Response({"data":serializer.data}, status=200)
    
    def patch(self, request, pk):
        # Partial update (only specified fields)
        blog_post = get_object_or_404(BlogPost, pk=pk)
        serializer = BlogPostGetSerializer(blog_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        # Full update (all fields required)
        blog_post = get_object_or_404(BlogPost, pk=pk)
        serializer = BlogPostGetSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        # Retrieve the BlogPost by its primary key
        blog_post = get_object_or_404(BlogPost, pk=pk)
        blog_post.delete()
        return Response({"detail": "Blog post deleted successfully."}, status=204)
    