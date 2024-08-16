from django.contrib import admin
from .models import Order, OrderItem, Address, CheckImage
from extensions.utils import jalali_converter
from django.utils.html import format_html


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class CheckImageInline(admin.TabularInline):
    model = CheckImage
    raw_id_fields = ['order']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['code', 'show_created', 'is_paid', 'shipping_status',
    'address', 'payment_type', 'ref_id', 'show_detail']

    list_filter = ('user', 'created', 'paid_time', 'is_paid', 'shipping_status', 'address', 'payment_type')
    inlines = [OrderItemInline, CheckImageInline]

    def show_detail(self, obj):
        return format_html(f"<a href='{ obj.get_absolute_url_for_admin() }'>کلیک کنید</a>",)

    def show_created(self, obj):
        return jalali_converter(obj.created)

    
    show_detail.short_description = 'نمایش جزئیات سفارش'
    show_created.short_description = 'زمان ایجاد'
    show_detail.allow_tags = True



admin.site.register(Address)
