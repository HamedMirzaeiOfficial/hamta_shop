from django import forms
from .models import User
from order.models import Address
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number')

        widgets = {
            'first_name': forms.TextInput(attrs={'dir': 'rtl', 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'dir': 'rtl', 'class': 'form-input'}), 
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
        }


    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('این شماره قبلا ثبت نام کرده است')
   
        return phone_number




class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'ssn')
        


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(label='کد تایید')



class LoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(), label="شماره تلفن")

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if not user:
            raise ValidationError('این شماره تلفن ثبت نام نکرده است.')
   
        return phone_number




class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'email',
         'is_active', 'ssn', 'wallet_amount', 'is_admin', 'is_superuser', 'password')


