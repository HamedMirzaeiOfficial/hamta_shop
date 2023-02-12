from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),   
    path('profile_address/', views.ProfileAddress.as_view(), name='profile_address'),
    path('profile_address_create/', views.ProfileAddressCreate.as_view(), name='profile_address_create'), 
    path('profile_address_update/', views.ProfileAddressUpdate.as_view(), name='profile_address_update'),
    path('profile_order/', views.profile_order, name='profile_order'), 
    path('profile_order_detail/<int:pk>/', views.profile_order_detail, name='profile_order_detail'), 
    path('profile_personal_info/', views.ProfilePersonalInfo.as_view(), name='profile_personal_info'), 
    path('profile_comment/', views.profile_comment, name='profile_comment'), 
    path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    
]