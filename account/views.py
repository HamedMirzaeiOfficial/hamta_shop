from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from order.models import Order
from .mixins import SuperUserAccessMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import User, OtpCode
from .forms import ProfileForm, UserRegistrationForm, VerifyCodeForm, LoginForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from order.models import Address, Order
from shop.models import Comment
from django.contrib.auth.decorators import login_required
import random
from extensions.utils import send_otp_code
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm



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
        return super().form_valid(form)


class ProfileAddressUpdate(LoginRequiredMixin, UpdateView):
    model = Address
    fields = ['title', ]
    template_name = 'account/profile_address_update.html'
    success_url = reverse_lazy('account:profile_address')

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



def login(request):
    form = None
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = 'شما با موفقیت وارد شدید'
                return redirect(reverse_lazy('account:profile'))
            else:
                message = 'ورود انجام نشد'
    return render(
        request, 'registration/login.html', context={'form': form, 'message': message})

class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')




@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterView(View):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {'first_name': form.cleaned_data['first_name'], 
                        'last_name': form.cleaned_data['last_name'], 'phone_number': form.cleaned_data['phone_number'], 
                        'password': form.cleaned_data['password1'], }

            messages.success(request, 'کد فعالسازی حساب کاربری برای شماره تلفن شما فرستاده شد.', 'success')
            return redirect('verify_code')

        return render(request, self.template_name, {'form': form})





class UserRegisterVerify(View):
    form_class = VerifyCodeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'registration/verify.html', {'form': form})


    def post(self, request, *args, **kwargs):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.filter(phone_number=user_session['phone_number']).last()
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                user = User.objects.create_user(first_name=user_session['first_name'], last_name=user_session['last_name'], phone_number=user_session['phone_number'], password=user_session['password'])
                user.is_active = True
                user.save()
                code_instance.delete()
                messages.success(request, 'ثبت نام شما با موفقیت انجام شد.', 'success')
                return redirect('login')

            else:
                messages.error(request, 'کد وارد شده اشتباه است.', 'danger')
                return redirect('verify_code')

        return redirect('shop:home')


