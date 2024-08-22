from django.db import models
# from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title   = models.CharField(max_length=100)
    content = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    auther  = models.ForeignKey(User,on_delete=models.CASCADE,default=6)
    image   = models.ImageField(upload_to='blog_images/',default='default_image.jpg')

    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    auther  = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')