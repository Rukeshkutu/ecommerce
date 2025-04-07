from django.db import models
from django.utils.text import slugify
from djanog.utils.crypto import get_random_string
from django.urls import reverse
from account.models import Account
from django.db.models import Avg, Count
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique= True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.category_name)
            slug = slug_base
            while Category.objects.filter(slug=slug).exixts():
                slug = f'{slug_base}-{get_random_string(10)}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.category_name

    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(max_length=800, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.product_name)
            slug = slug_base
            while Product.objects.filter(slug=slug).exixts():
                slug = f'{slug_base}-{get_random_string(10)}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class VariationManager(models.Model):
    def colors(self):
        return super(VariationManager, self).filter(variation_category = 'color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category = 'size', is_active = True)

variation_category =(
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now = True)

    object = VariationManager()
    
    def __str__(self):
        return self.variation_value
    
class ReviewRating(models.Model):
    # RATING_CHOICES = [
    #     (1,'1 - Poor'),
    #     (2,'2 - Fair'),
    #     (3,'3 - Good'),
    #     (4,'4 - Very Good'),
    #     (5, '5 - Excellent'),
    # ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField()
    review = models.TextField(max_length=400, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"{self.user.username}'s review on {self.product.product_name}"
    
    class Meta:
        unique_together = ["user", "product"]
        ordering = ["-created"]


