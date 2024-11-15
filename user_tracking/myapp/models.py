from django.db import models
from django.contrib.auth.models import User
from .mixins import TrackableMixin


class Product(TrackableMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return self.name

class Order(TrackableMixin):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices = (('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')), default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.customer.username} - {self.product.name}"

class CustomerProfile(TrackableMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.user.username

class TodoTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    model_instance_id = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
    
    class Meta:
        verbose_name = 'Todo Tracking'
        verbose_name_plural = 'Todo Tracking'
        ordering = ['-timestamp']