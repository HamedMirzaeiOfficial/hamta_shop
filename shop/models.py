from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField 
from decimal import Decimal
from django.utils import timezone
from account.models import User
from django.contrib.contenttypes.fields import GenericRelation
from extensions.utils import jalali_converter


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).get_queryset().filter(available=True)



class AcceptedManager(models.Manager):
    def get_queryset(self):
        return super(AcceptedManager, self).get_queryset().filter(status='accepted')



class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="اسلاگ دسته بندی")
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True, verbose_name="والد دسته بندی")

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"


    def __str__(self):
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])  


    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])



class Product(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name="نام محصول")
    english_name = models.CharField(max_length=100, db_index=True, verbose_name="نام انگلیسی")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="دسته بندی محصول")
    slug = models.SlugField(unique=True, db_index=True, verbose_name="اسلاک محصول")
    brand = models.CharField(max_length=100, verbose_name="برند محصول")
    guarantee = models.PositiveIntegerField(verbose_name="گارانتی محصول")
    available = models.BooleanField(default=True, verbose_name="موجود است؟")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    price_after_discount = models.PositiveIntegerField(default=0, verbose_name="قیمت بعد از تخفیف")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    discount = models.PositiveIntegerField(verbose_name="درصد تخفیف")
    discount_time = models.DateTimeField(verbose_name="تخفیف تا تاریخ")
    delivery = models.PositiveIntegerField(verbose_name="تحویل چند روزه؟")
    number_sold = models.BigIntegerField(default=0, verbose_name="تعداد فروخته شده")


    objects = models.Manager()
    objects_available = AvailableManager()
    
    class Meta:
        ordering = ('-created', )
        index_together = (('id', 'slug'), ) 
        verbose_name = "محصول"
        verbose_name_plural = "محصول ها"


    def __str__(self):
        return self.title   


    def check_discount_time(self):
        return self.discount_time > timezone.now()
        
        
    def get_discount(self):
        if self.check_discount_time():
            return Decimal((self.discount * self.price)) / 100
        else:
            return 0
        

    def get_price_after_discount(self):
        return self.price - self.get_discount()


    def category_to_str(self):
	    return "، ".join([category.title for category in self.category.active()])
    
    category_to_str.short_description = "دسته‌بندی"


    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'id': self.id, 'slug': self.slug})


    def save(self, *args, **kwargs):
        self.price_after_discount = self.get_price_after_discount()
        return super().save(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        self.price_after_discount = self.get_price_after_discount()
        return super().update(*args, **kwargs)
    
    

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="مجصول مربوطه")
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name="عکس")

    class Meta:
        verbose_name = "عکس محصول"
        verbose_name_plural = "عکس های محصول"

    def __str__(self):
        return self.product.title


class Property(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='properties', verbose_name="محصول مربوطه")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    detail = models.CharField(max_length=100, verbose_name="جزئیات")

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"

    def __str__(self):
        return self.title


class Description(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='descriptions', verbose_name="محصول مربوطه")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    detail = HTMLField(verbose_name="جزئیات")

    class Meta:
        verbose_name = "توضیحات"
        verbose_name_plural = "توضیحات"

    def __str__(self):
        return self.title



class TechnicalDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='technical_descriptions', verbose_name="محصول مربوطه")
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True, verbose_name="والد جزئیات")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    detail = models.CharField(max_length=100, blank=True, verbose_name="جزئیات")
    
    class Meta:
        verbose_name = "مشخصات فنی"
        verbose_name_plural = "مشخصات فنی"

    def __str__(self):
        return self.title


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/%Y/%m/%d', verbose_name="عکس")
    link = models.URLField(verbose_name="لینک")

    class Meta:
        verbose_name = "بنر"
        verbose_name_plural = "بنر ها"

    def __str__(self):
        return self.link


class Comment(models.Model):
    STATUS = (
        ('waiting', 'در انتظار تایید'),
        ('accepted', 'تایید شده'),
        ('not accepted', 'تایید نشده')
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="محصول مربوطه")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="کاربر مربوطه")
    title = models.CharField(max_length=50, verbose_name="عنوان نظر")
    email = models.EmailField(max_length=200, blank=True, verbose_name="ایمیل")
    description = models.TextField(verbose_name="متن نظر")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد شدن")
    status = models.CharField(choices=STATUS, default='waiting', max_length=50, verbose_name="وضعیت")
    offer_vote = models.BooleanField(default=False, verbose_name="پیشنهاد میشود؟")

    objects = models.Manager()  # The default manager.
    accepted = AcceptedManager()  # Our custom manager.

    def jcreated_on(self):
        return jalali_converter(self.created_on)

    class Meta:
        ordering = ('-created_on', ) 
        verbose_name = "نظر"
        verbose_name_plural = "نظر ها"

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product}'



class Contact(models.Model):
    CHOICES = (
        ('PROPOSAL', 'پیشنهاد'),
        ('COMPLAINT', 'انتقاد یا شکایات'),
        ('FOLLOW', 'پیگیری سفارش'),
        ('SERVICE', 'خدمات پس از فروش'),
        ('MANAGE', 'مدیریت'),
        ('OTHER', 'سایر موضوعات'), 
    )

    subject = models.CharField(max_length=100, choices=CHOICES, verbose_name="عنوان")
    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.BigIntegerField(verbose_name="شماره تلفن")
    message = models.TextField(verbose_name="متن پیام")

    class Meta: 
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

    def __str__(self):
        return self.name + " ==> " + self.message[0:20] + " ... " 



    



