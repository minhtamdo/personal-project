from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    phone_number  = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
    
class Subcategory(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="category")

    def __str__(self):
        return f"{self.name}"
    
class ProductClass(models.Model):
    name = models.CharField(max_length=64)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=False, related_name="product_class")

    def __str__(self):
        return f"{self.name}"

class Color(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Size(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
    
class Item(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, null=False, related_name="product_classify")
    image = models.ImageField(upload_to="uploads/items/",null=True, blank=True)
    specifications = models.ImageField(upload_to="uploads/items/",null=True, blank=True)
    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    name = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, related_name="general_name")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.BigIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, related_name="product_color")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, related_name="product_size")
    image = models.ImageField(upload_to="uploads/items/",null=True, blank=True)
    def __str__(self):
        return f"{self.name}"

class Wishlist(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.owner}'s Wishlist"
    
class Cart(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.quantity * self.name.price

    def __str__(self):
        return f"{self.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 999.99
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    
    
class Region(models.Model):
    name = models.TextField()

    def __str__(self):
        return f"{self.name}"
    
class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False, related_name="order_shipment")
    shipment_date = models.DateTimeField()
    address = models.TextField(blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False, related_name="shipping_region")
    postal_code = models.CharField(max_length=8)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, related_name="order_product")
    quantity = models.BigIntegerField()
    order = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, related_name="in_order")
    price = models.DecimalField(max_digits=12, decimal_places=2)

class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username}: {self.text[:20]}'






    

