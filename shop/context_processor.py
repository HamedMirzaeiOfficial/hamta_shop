from .models import Category


def categories(request):
    return {'categories': Category.objects.filter(parent=None)}
def show_min_time_discount(request):
    return {'min_time': Product.objects_available.order_by('discount_time').first().discount_time.utcfromtimestamp(0)}


def show_categories_in_footer(request):
    return {'categories_footer': Category.objects.all()[0:9]}

