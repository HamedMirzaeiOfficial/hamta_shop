from django.contrib import admin
from .models import Order, OrderItem, Address, CheckImage


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class CheckImageInline(admin.TabularInline):
    model = CheckImage
    raw_id_fields = ['order']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('user', 'created', 'paid_time', 'is_paid', 'shipping_status', 'address', 'payment_type', )
    inlines = [OrderItemInline, CheckImageInline]



admin.site.register(Address)
