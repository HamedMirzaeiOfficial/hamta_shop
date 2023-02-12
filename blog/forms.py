from django import forms
from .models import Comment


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