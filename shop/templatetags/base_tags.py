from django import template
from ..models import Category


register = template.Library()



@register.inclusion_tag("shop/category_navbar.html")
def category_navbar():
	return {
		"categories": Category.objects.filter(parent=None)
	}



@register.filter
def objects(t, product):
    return t.objects.filter(product=product)
