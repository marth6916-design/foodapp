from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurant_images/')
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Food(models.Model):
    CATEGORY_CHOICES = [
        ('Burgers', 'Burgers'),
        ('Pizza', 'Pizza'),
        ('Drinks', 'Drinks'),
        ('Sides', 'Sides'),
        ('Desserts', 'Desserts'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='food_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Burgers')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username} - {self.food.name}"
    
    def total_price(self):
        return self.quantity * self.food.price

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('On the Way', 'On the Way'),
        ('Delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20, default='Cash on Delivery')
    address = models.TextField()

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.name} - {self.rating}⭐"