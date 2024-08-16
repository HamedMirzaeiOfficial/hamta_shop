from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from cart.cart import Cart
from .models import OrderItem, Order, Address
import uuid
from django.utils import timezone
from .forms import PaymentTypeForm, CheckForm
from django.contrib.auth.decorators import login_required


@login_required
def order_process(request):
    address = None
    try:
        address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        address = None

    if not address:
        return redirect('account:profile_address_create')
    
    if request.method == 'POST':
        form = PaymentTypeForm(request.POST)
        if form.is_valid():
            payment_type = form.cleaned_data['payment_type']
            request.session['payment_type'] = payment_type  
            request.session.modified = True
            description = form.cleaned_data['description']
            request.session['description'] = description
            request.session.modified = True
            return redirect('order:order_create')
        
    else:
        form = PaymentTypeForm()
    
    return render(request, 'order/order_process.html', {'form': form, 'address': address})


    

@login_required
def order_create(request):
    cart = Cart(request)
    address = None
    order = None

   

    try:
        address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        address = None

    try:
        order = Order.objects.get(user=request.user, pk=request.session['order_id'])
        if order.payment_type != request.session['payment_type']:
            order.payment_type = request.session['payment_type']
            order.save()
    except:
        order = Order.objects.create(user=request.user, address=address, payment_type=request.session['payment_type'])

    
    
    
    
    order.description = request.session['description']
    order.save()


    if request.session['payment_type'] == 'Home':
        order.shipping_status = 'Posted'
        order.save()

    for item in cart:
        OrderItem.objects.create(order=order,
                                    product=item['product'],
                                    price=item['price'],
                                    price_after_discount=item['price_after_discount'], 
                                    quantity=item['quantity'])
        

    for item in order.items.all():
        item.product.number_sold += item.quantity
        item.product.save()
        item.save()

    cart.clear()
    request.session['order_id'] = order.id
    request.session.modified = True
 
    return render(request, 'order/order_create.html',
                      {'order': order})



@login_required
def check_payment_form(request):
    if request.method == 'POST':
        form = CheckForm(request.POST, request.FILES)
        if form.is_valid():
            order = Order.objects.get(id=request.session['order_id'])
            order.shipping_status = 'Waiting For Checking'
            order.save()
            object_form = form.save(commit=False)
            object_form.order = order
            object_form.save()
            request.session.pop('order_id', None)
            return redirect('account:profile_order') # redirect to success page
    
    else:
        form = CheckForm()

    
    return render(request, 'order/check_payment_form.html', {'form': form})



@login_required
def admin_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order/admin_order_detail.html', {'order': order})


