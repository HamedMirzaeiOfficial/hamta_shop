from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from order.models import Order
from .mixins import SuperUserAccessMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import User
from .forms import ProfileForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from order.models import Address, Order
from shop.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import SignUpForm
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.messages.views import SuccessMessageMixin


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'ssn']
    template_name = 'account/profile.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.request.user.orders.all()[0:6]
        return context


class ProfileAddress(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            address = None
        return render(request, 'account/profile_address.html', {'address': address})


class ProfileAddressCreate(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['title', ] 
    template_name = 'account/profile_address_create.html'
    success_url = reverse_lazy('account:profile_address')

    def get_object(self):
        return Address.objects.get_or_create(user=self.request.user) 
        

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()        
        messages.success("آدرس ایجاد گردید")
        return super().form_valid(form)


class ProfileAddressUpdate(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    model = Address
    fields = ['title', ]
    template_name = 'account/profile_address_update.html'
    success_url = reverse_lazy('account:profile_address')
    success_message = 'تغییرات ثبت گردید'

    def get_object(self):
        return Address.objects.get(user=self.request.user) 
        

@login_required
def profile_order(request):
    paid_orders = request.user.orders.filter(shipping_status='Paid')
    waiting_payment_orders = request.user.orders.filter(shipping_status='Waiting Payment')
    posted_orders = request.user.orders.filter(shipping_status='Posted')
    waiting_for_checking_orders = request.user.orders.filter(shipping_status='Waiting For Checking')
    delivered_orders = request.user.orders.filter(shipping_status='Delivered') 
    returned_orders = request.user.orders.filter(shipping_status='Returned')
    canceled_orders = request.user.orders.filter(shipping_status='Canceled')
    

    context = {'paid_orders': paid_orders, 'waiting_payment_orders': waiting_payment_orders,
               'posted_orders': posted_orders, 'waiting_for_checking_orders': waiting_for_checking_orders, 
               'delivered_orders': delivered_orders, 'returned_orders': returned_orders, 
               'canceled_orders': canceled_orders, }

    return render(request, 'account/profile_order.html', context)


@login_required
def profile_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'account/profile_order_detail.html', {'order': order})



class ProfilePersonalInfo(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'account/profile_personal_info.html'
    success_url = reverse_lazy('account:profile_personal_info')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk) 


@login_required
def profile_comment(request):
    comments = request.user.comments.all()
    return render(request, 'account/profile_comment.html', {'comments': comments})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:
        comment.delete()

    return redirect('account:profile_comment')


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')




class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')


class Register(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'activate your account'
        message = render_to_string('registration/activate_Account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return render(self.request, 'registration/send_email.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/confirm_or_not_activate.html', {'active': True})
    else:
        return render(request, 'registration/confirm_or_not_activate.html', {'active': False})


