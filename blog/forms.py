from django import forms
from .models import Blog,Comment

# views code 

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Content', 'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Comment', 'class': 'form-control'}),
        }
        labels = {
            'text': 'Comment',
        }