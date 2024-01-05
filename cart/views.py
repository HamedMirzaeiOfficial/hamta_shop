from django.shortcuts import render, redirect, HttpResponse
from shop.models import Product
from django.contrib.auth.decorators import login_required
from .cart import Cart


@login_required
def item_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    product.get_discount()
    cart.add(product=product)
    params = request.GET.copy()
    search_value = request.GET.get('q', None)
    if search_value:
        params['q'] = search_value
    
    referrer_url = request.META.get('HTTP_REFERER', '/')  # Get the referrer URL, default to '/' if not found
    if request.GET.get('next') is None:
        return redirect(referrer_url)
    return redirect(request.GET.get('next'))


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart:cart_detail")


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)

    referrer_url = request.META.get('HTTP_REFERER', '/')  # Get the referrer URL, default to '/' if not found
    if request.GET.get('next') is None:
        return redirect(referrer_url)
    return redirect(request.GET.get('next'))
   
   
@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    referrer_url = request.META.get('HTTP_REFERER', '/')  # Get the referrer URL, default to '/' if not found
    if request.GET.get('next') is None:
        return redirect(referrer_url)
    return redirect(request.GET.get('next'))
   
@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    referrer_url = request.META.get('HTTP_REFERER', '/')  # Get the referrer URL, default to '/' if not found
    if request.GET.get('next') is None:
        return redirect(referrer_url)
    return redirect(request.GET.get('next'))
   

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html')