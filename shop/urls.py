from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('search/', views.SearchList.as_view(), name="search"),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.ProductListByCategory.as_view(), name='product_list_by_category'), 
    path('product_offer_list/', views.product_offer_list, name='product_offer_list'), 
    path('contact_us/', views.ContactView.as_view(), name='contact'),
]