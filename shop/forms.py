from django import forms
from tinymce.widgets import TinyMCE
from django.core.exceptions import ValidationError
from .models import Contact, Comment, Description


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 100, 'rows': 160}
        )
    )
    class Meta:
        model = Description
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('subject', 'name', 'phone', 'email', 'message')
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}), 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}), 
            'message': forms.Textarea(attrs={'class': 'form-control'}), 
        }

        labels = {
            'subject': 'موضوع را انتخاب کنید',
            'name': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'phone': 'شماره تماس',
            'message': 'پیام',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'email', 'description', 'offer_vote']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-element'}),
            'email': forms.EmailInput(attrs={'class': 'input-element'}),
            'description': forms.Textarea(attrs={'class': 'input-element'}), 
            'offer_vote': forms.CheckboxInput()
        }
        labels = {
            'title': 'عنوات نظر شما(اجباری)',
            'email': 'ایمیل شما',
            'description': 'نظر شما',
            'offer_vote': 'خرید این محصول را پیشنهاد میکنید',
        }




    def __init__(self, *args, **kwargs):
        """Save the request with the form so it can be accessed in clean_*()"""
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)


   
class ColorForm(forms.Form):
    color = forms.TextInput()
    