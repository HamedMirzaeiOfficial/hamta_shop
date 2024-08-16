from django.urls import path
from . import views
app_name = 'order'


urlpatterns = [
    path('process/', views.order_process, name='order_process'), 
    path('create/', views.order_create, name='order_create'),
    path('check_payment_form/', views.check_payment_form, name='check_payment_form'), 
    path('order_detail/<int:pk>/', views.admin_order_detail, name='admin_order_detail')

]