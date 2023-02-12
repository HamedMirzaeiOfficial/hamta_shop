from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import Product, Banner, Category, Comment, Contact
from django.db.models import Q
from .forms import CommentForm, ContactForm
from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone


class Home(View):
    def get(self, request):
        last_products = Product.objects_available.all()[:20]
        best_sellers_products = Product.objects_available.order_by('-number_sold')[:9] 
        offer_products = Product.objects_available.filter(~Q(discount=0), discount_time__gte=timezone.now())[:10]
        banners = Banner.objects.all()
        
        return render(request, 'shop/home.html', 
                {'last_products': last_products, 
                'best_sellers_products': best_sellers_products,
                'offer_product': offer_products, 
                'banners': banners,
        })
        

    
class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        view = ProductDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProductComment.as_view()
        return view(request, *args, **kwargs)



class ProductDisplay(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['technical_descriptions'] = context['product'].technical_descriptions.filter(parent=None)
        context['similar_products'] = Product.objects.filter(category=context['product'].category)
        context['comments'] = Comment.accepted.filter(product=self.get_object())
        return context



class ProductComment(SingleObjectMixin, FormView):
    model = Product
    form_class = CommentForm
    template_name = 'shop/product_detail.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


    def get_form_kwargs(self):
        kwargs = super(ProductComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.product = self.object
        comment.user = self.request.user
        comment.save()
        
        return super().form_valid(form)


    def get_success_url(self):
        messages.success(self.request, "A comment has been sent.")
        return reverse('shop:product_detail', kwargs={'id': self.object.id,
                                                      'slug': self.object.slug})



class SearchList(ListView):
	paginate_by = 200
	template_name = 'shop/search_list.html'

	def get_queryset(self):
		search = self.request.GET.get('q')
		return Product.objects_available.filter(Q(descriptions__detail__icontains=search) | Q(title__icontains=search) | Q(technical_descriptions__detail__icontains=search))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search'] = self.request.GET.get('q')
		return context



class ProductListByCategory(View):
    def get(self, request, *args, **kwargs):
        category_slug = self.kwargs.get('slug')
        category = Category.objects.get(slug=category_slug)
        if category.parent is None:
            products = Product.objects_available.filter(category__parent__slug=category_slug)
        else:
            products = category.products.filter(available=True)

        return render(request, template_name='shop/product_list_by_category.html', context={'products': products, 'category': category})



def product_offer_list(request):
    products = Product.objects_available.filter(~Q(discount=0), discount_time__gte=timezone.now())
    return render(request, 'shop/product_offer_list.html', {'products': products})



class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'shop/contact.html'

    def get_success_url(self) -> str:
        success_message = 'پیام شما به دست ما رسید.'
        messages.success(self.request, success_message)
        return reverse('shop:contact')
        
   