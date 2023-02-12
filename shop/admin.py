from django.contrib import admin
from .models import Product, Category, Image, Property, Description, TechnicalDescription, Contact, Banner, Comment

admin.site.site_header = 'فروشگاه موبایل'


class CommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['product']


class PropertyInline(admin.TabularInline):
    model = Property
    raw_id_fields = ['product']


class ImageInline(admin.TabularInline):
    model = Image
    raw_id_fields = ['product']


class DescriptionInline(admin.TabularInline):
    model = Description
    raw_id_fields = ['product']


class TechnicalDescriptionInline(admin.TabularInline):
    model = TechnicalDescription
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'brand', 'available', 'created', 'updated', 'discount', 'discount_time', 'delivery')
    inlines = [PropertyInline, ImageInline, DescriptionInline, TechnicalDescriptionInline, CommentInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_filter = ('subject', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ('product', 'user', 'created_on', 'status', 'offer_vote')



admin.site.register(Category)

admin.site.register(Banner)
