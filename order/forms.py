from django import forms
from .models import Order, CheckImage


class PaymentTypeForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('payment_type', 'description')

        labels = {
            'payment_type': 'نحوه ی پرداخت', 
            'description': 'اگر توضیحاتی درباره ی رنگ سفارشات دارید اینجا بنویسید',
        } 


class CheckForm(forms.ModelForm):
    class Meta:
        model = CheckImage
        fields = ('check_image', 'national_cart', 'others')

        
        labels = {
            'check_image': 'عکس چک', 
            'national_cart': 'عکس کارت ملی', 
            'others': 'سایر مدارک'
        }   