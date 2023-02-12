from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('process/<int:order_id>/', views.PaymentView.as_view(), name='process'), 
    path('verify/', views.VerifyView.as_view(), name='verify'), 
    path('success_payment_home/', views.success_payment_home, name='success_payment_home'), 

]
