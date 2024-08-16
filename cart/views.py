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
    if request.GET.get('next') is None:
        return redirect('shop:home')
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
    return redirect(product.get_absolute_url())


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect(product.get_absolute_url())


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html')