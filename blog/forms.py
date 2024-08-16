from django import forms
from .models import Comment, Post
from tinymce.widgets import TinyMCE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'email', 'body']
        labels = {
        'title': 'عنوان نظر شما', 
        'email': 'ایمیل شما', 
        'body': 'نظر شما' 
        }


class SearchForm(forms.Form):
    query = forms.CharField()


class FlatPageForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'publish', 'slug')
        widgets = {'body': TinyMCE()}