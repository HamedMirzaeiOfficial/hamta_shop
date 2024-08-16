from .models import Category, Banner


def categories(request):
    return {'categories': Category.objects.filter(parent=None)}


def show_categories_in_footer(request):
    return {'categories_footer': Category.objects.all()[0:9]}


def banners(request):
    return {'banners': Banner.objects.all()}
