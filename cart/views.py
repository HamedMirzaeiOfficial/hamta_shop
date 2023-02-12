from django.shortcuts import render, redirect
from shop.models import Product
from django.contrib.auth.decorators import login_required
from .cart import Cart


@login_required
def item_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    product.get_discount()
    cart.add(product=product)
    return redirect("shop:home")


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("shop:home")


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart:cart_detail")


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart:cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html')