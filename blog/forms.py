from django import forms
from .models import Blog,Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# views code 

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content','image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            'content': forms.CharField(widget=CKEditorUploadingWidget())
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