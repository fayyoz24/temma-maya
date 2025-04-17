from django.db import models
from users.models import User
import re
from bs4 import BeautifulSoup
# Create your models here.

BLOG_TYPE_CHOICES = [('SI', 'STUDY INSIGHTS'), ('CR', 'CAREER INSIGHTS'), 
                      ('CI', 'COMPANY INSIGHTS'), ('CC', 'COMPANY COMPARISON'), 
                      ('SC', 'STUDIES COMPARISON')]


class BlogPost(models.Model):

    blog_choice = models.CharField(max_length=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    featured = models.BooleanField(default=False)
    image_1 = models.URLField()
    path_1 = models.CharField(max_length=200)
    image_2 = models.URLField(null=True, blank=True)
    path_2 = models.CharField(max_length=200, null=True, blank=True)
    name_1 = models.CharField(max_length=100, null=True, blank=True)
    name_2 = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    views_num = models.PositiveIntegerField(default=0)

    def all_titles(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        h2_h3_texts = [tag.get_text() for tag in soup.find_all(['h2'])]
        return h2_h3_texts
        # return re.findall(r'<h[23]>(.*?)</h[23]>', self.content, re.DOTALL)
    
    def __str__(self) -> str:
        return self.blog_choice + " " + self.title