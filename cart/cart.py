from decimal import Decimal
from django.conf import settings
from shop.models import Product
from django.shortcuts import redirect
from django.utils import timesince

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)


        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product


        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['price_after_discount'] = int(item['price_after_discount'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())


    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price), 
                                     'price_after_discount': str(product.price_after_discount)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()


    def save(self):
        # Update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True


    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def decrement(self, product):
        for key in self.cart:
            if key == str(product.id):
                self.cart[str(product.id)]['quantity'] -= 1
                if self.cart[str(product.id)]['quantity'] < 1:
                    return redirect('cart:cart_detail')
                self.save()
                break
            else:
                print("Something Wrong")


    def clear(self):
        # remove cart from session
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True


    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    
    def get_total_price_after_discount(self):
        return sum(int(item['price_after_discount']) * item['quantity'] for item in self.cart.values())


    def get_discount_price(self):
        return self.get_total_price() - self.get_total_price_after_discount()