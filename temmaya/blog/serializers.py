from rest_framework import serializers
from .models import BlogPost

class BlogPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ['creator']
        
class BlogPostGetSerializer(serializers.ModelSerializer):
    # Define a method field for all_titles
    all_titles = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'blog_choice', 'title', 
                  'short_desc','content', 'featured', 'image_1',
                  'path_1','path_2',
                  'image_2', 'name_1', 'name_2', 'created_at',
                  'views_num', 'all_titles']

    def get_all_titles(self, obj):
        # Call the `all_titles` method from the BlogPost instance
        return obj.all_titles()