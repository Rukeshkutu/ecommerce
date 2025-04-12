from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.urls import reverse
from account.models import Account, Vendor
from django.db.models import Avg, Count
from Ecommerce import settings
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique= True)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank=True, related_name='subcategories')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.category_name)
            slug = slug_base
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f'{slug_base}-{get_random_string(10)}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.category_name

    
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE, related_name = 'products' )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'products')
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(max_length=800, blank=True)
    price = models.DecimalField(max_digits = 100, decimal_places = 2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='media/product', blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.product_name)
            slug = slug_base
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{slug_base}-{get_random_string(10)}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.product_name

class Order(models.Model):
    customer = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'orders')
    products = models.ForeignKey(Product, through =  'OrderItem')
    total_price = models.DecimalField(max_digits = 100, decimal_places = 2)
    shipping_address = models.FileField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete =  models.CASCADE, related_name = 'items')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

class Cart (models.Model):
    user = models.ForeignKey(Account, on_delete= models.CASCADE, related_name = 'cart', null=True, blank=True)
    session_id = models.CharField(max_length = 100, null=True, blank=True)
    items = models.ManyToManyField(Product, through='CartItem')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name = 'items')
    product = models.ManyToManyField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

class Shipping(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    rate = models.DecimalField(max_digits = 10, decimal_places=2)

class Payment(modls.Model):
    order = models.ForeignKey(Order, on_delete =  models.CASCADE, related_name = 'payment')
    method = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    transaction_id = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)

class Coupon(models.Model):
    code = models.CharField(max_length = 100, unique = True)
    discount = models.DecimalField(max_digits = 10, decimal_paces = 2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

class Review(models.Model)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "reviews")
    customer = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class Wishlist(models.Model)
    user = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'wishlist')
    product = models.ForeignKey(Product, related_name = "wishlist")

class Notification(modles.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'notifications')
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    title = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, unique = True)
    content = models.TextField()
    auther = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = 'blog_posts')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class FQA(models.Model):
    question = models.TextField()
    answer = models.TextField()

class Analytics(models.Models):
    sales = models.DecimalField(max_digits = 10, decimal_places = 2)
    traffic = models.PositiveBigIntegerField()
    popular_products = models.ManyToManyField(Product, related_name = 'analytics')
    created_date = models.DateTimeField(auto_now_add=True)

class Configuration(models.Model):
    site_name = models.CharField(max_length = 100)
    site_description = models.TextField()
    site_logo = models.ImageField(upload_to = 'media/logos')

class Tax(models.Model):
    name = models.CharField (max_length = 100)
    rate = models.DecimalField(max_digits = 5, decimal_places = 2)
    country = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100, null = True, blank = True)

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscibed_at = models.DateTimeField(auto_now_add = True)

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete =  models.CASCADE, related_name = 'refund')
    reason = models.TextField()
    amount = models.DecimalField(max_digits = 5, decimal_palaces = 2)
    status = models.CharField(max_length = 100)
    requested_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True, blank = True)