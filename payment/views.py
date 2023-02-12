from django.views import View
from django.shortcuts import render, redirect
from .zarinpal import zpal_request_handler, zpal_payment_checker
from django.conf import settings
from order.models import Order
from django.shortcuts import get_object_or_404
from cart.cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone


class PaymentView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        return render(request, 'order/order_create.html', {'order': order})   
    

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        payment_link, authority = zpal_request_handler(settings.ZARINPAL['merchant_id'], order.get_total_cost_after_discount(),
                                                            'فروشگاه اینترنتی', order.user.email, order.user.phone_number, 
                                                             settings.ZARINPAL['gateway_callback_url'])
        
        request.session.pop('order_id', None) 

        request.session['order_id_for_verify'] = order.id
        request.session.modified = True
        

        if payment_link is not None:
            return redirect(payment_link)

        return render(request, 'order/order_create.html')



class VerifyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=request.session['order_id_for_verify'])
        authority = request.GET.get('Authority')
        is_paid, ref_id = zpal_payment_checker(settings.ZARINPAL['merchant_id'], order.get_total_cost_after_discount(), authority)

        if is_paid:
            order.is_paid = True
            order.shipping_status = 'Paid'
            order.ref_id = ref_id
            order.paid_time = timezone.now()
            order.save()
        

        if is_paid:
            return render(request, 'payment/success.html', {'order': order, 'ref_id': ref_id})  
        else:
            return render(request, 'payment/failure.html', {'order': order, 'ref_id': ref_id})  
            
        

@login_required
def success_payment_home(request):
    try:
        order = Order.objects.get(pk=request.session['order_id'])
    except:
        return redirect('account:profile_order')
    request.session.pop('order_id', None)
    return render(request, 'payment/success.html', {'order': order})