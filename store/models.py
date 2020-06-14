from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import *
from django.dispatch import receiver

CATEGORY_CHOICES = (
    ('Bo', 'Bolsas'),
    ('Ci', 'Cintos'),
    ('Ca', 'Carteiras'),
    ('Es', 'Escolar'),
    ('Ar', 'Armarinho'),
    ('Br', 'Briquedos'),
    ('Ac','Acessorio'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, null= True, blank= True, on_delete= models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name 


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null= True, blank= True)
    discount_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField()
    image = models.ImageField(null=True, blank= True)
    description = models.TextField()


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            'slug': self.slug
        })

    def get_real_price(self):
        return self.price - self.discount_price
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, null=True, blank= True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null= True)
    quantity = models.IntegerField(default=0, null=True, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity

        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null= True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null= True)
    address = models.CharField(max_length= 200, null= False)
    city = models.CharField(max_length= 200, null= False)
    state = models.CharField(max_length= 200, null= False)
    zipcode  = models.CharField(max_length= 200, null= False)
    date_added  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address