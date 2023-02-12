"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from account.views import login, UserRegisterView, UserRegisterVerify



urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify/', UserRegisterVerify.as_view(), name='verify_code'),
    path('tinymce/', include('tinymce.urls')),
    path('', include('shop.urls', namespace='home')),
    path('cart/', include('cart.urls', namespace='cart')),  
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/', include('account.urls', namespace='accounts')),
    path('order/', include('order.urls', namespace='order')),
    path('account/', include('account.urls', namespace='account')),
    path('payment/', include('payment.urls', namespace='payment')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)