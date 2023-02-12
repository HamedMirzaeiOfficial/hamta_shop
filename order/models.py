from django.db import models
from account.models import User
from shop.models import Product
import uuid
from extensions.utils import jalali_converter
from django.urls import reverse


class Address(models.Model):
    title = models.CharField(max_length=300, verbose_name="آدرس دقیق")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر منتسب به آدرس")

    
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"


    def __str__(self):
        return self.user.get_full_name() + "  -->  " + self.title




class Order(models.Model):
    STATUS = (
        ('Waiting Payment', 'در انتظار پرداخت'),
        ('Paid', 'پرداخت شده'),
        ('Posted', 'ارسال شده'), 
        ('Delivered', 'تحویل داده شده'), 
        ('Returned', 'مرجوعی'), 
        ('Canceled', 'لغو شده'), 
        ('Waiting For Checking', 'منتظر تایید شدن چک')
    )

    PAYMENT_TYPE = (
        ('Internet', 'پرداخت اینترنتی'), 
        ('Home', 'پرداخت در محل'), 
        ('Check', 'خرید چکی'), 
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="کاربر سفارش دهنده")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    paid_time = models.DateTimeField(null=True, blank=True, verbose_name="زمان پرداخت")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده؟")
    code = models.UUIDField(default=uuid.uuid4, editable=False, max_length=15, verbose_name="کد")
    shipping_status = models.CharField(choices=STATUS, max_length=20, default='Waiting Payment', verbose_name="وضعیت سفارش")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders', verbose_name="آدرس")
    payment_type = models.CharField(choices=PAYMENT_TYPE, default='Internet', max_length=100, verbose_name="نوع پرداخت")
    ref_id = models.IntegerField(blank=True, null=True, verbose_name="کد رهگیری پرداخت اینترنتی")
    description = models.TextField(verbose_name="توضیحات مربوط به سفارش(رنگ کالا)")
    

    class Meta:
        ordering = ('-created', )
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"

    def __str__(self):
        return f"{self.code}"

    def get_absolute_url(self):
        return reverse('account:profile_order_detail', kwargs={'pk': self.id})


    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    
    def get_total_cost_after_discount(self):
        return sum(item.get_cost_after_discount() for item in self.items.all())

    def get_discount_cost(self):
        return self.get_total_cost() - self.get_total_cost_after_discount()


    def jpaid_time(self):
        return jalali_converter(self.paid_time)

    def jcreated(self):
        return jalali_converter(self.created)


    def show_payment_status(self):
        if self.payment_type == 'Internet':
            return 'پرداخت اینترنتی'
        elif self.payment_type == 'Home':
            return 'پرداخت در محل'
        else:
            return 'خرید چکی'


    def show_shipping_status(self):
        if self.shipping_status == 'Waiting Payment':
            return 'منتظر پرداخت'
        elif self.shipping_status == 'Waiting For Checking':
            return 'در انتظار تایید چک'
        elif self.shipping_status == 'Delivered':
            return 'تحویل داده شده'
        elif self.shipping_status == 'Returned':
            return 'برگشت داده شده'
        elif self.shipping_status == 'Canceled':
            return 'کنسل شده'
        elif self.shipping_status == 'Paid':
            return 'پرداخت شده'
        else:
            return 'ارسال شده'


    def show_paid(self):
        if self.is_paid:
            return True
        else:
            return False

    show_paid.boolean = True
    show_paid.short_description = "وضعیت پرداخت"

   

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش مربوطه")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.RESTRICT, verbose_name="محصول مربوطه")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    price_after_discount = models.PositiveIntegerField(verbose_name="قیمت بعد از تخفیف")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    class Meta:
        verbose_name = "آیتم"
        verbose_name_plural = "آیتم ها"
  
    
    def __str__(self):
        return str(self.id)


    def get_cost(self):
        return self.price * self.quantity


    def get_cost_after_discount(self):
        return self.price_after_discount * self.quantity




class CheckImage(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="سفارش مربوطه")
    check_image = models.ImageField(upload_to='check/check_image/', verbose_name="عکس چک") 
    national_cart = models.ImageField(upload_to='check/national_cart/', verbose_name="عکس کارت ملی")
    others = models.ImageField(blank=True, null=True, upload_to='check/others', verbose_name="سایر مدارک")

    def __str__(self):
        return str(self.order.code)

        
    class Meta:
        verbose_name = "چک  "
        verbose_name_plural = "چک ها"
  