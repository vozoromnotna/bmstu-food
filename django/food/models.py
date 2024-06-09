from django.db import models
from django.contrib.auth.models import User

class ProductionType(models.TextChoices):
    WENDING = 'wending', 'Wending'
    BUFFET = 'buffet', 'Buffet'
    CAFE = 'cafe', 'Cafe'


class Foodservice(models.Model):
    title = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=10, choices=ProductionType.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default=None, blank=True)
    image = models.TextField(default=None, blank=True)
    foodservice = models.ForeignKey(Foodservice, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    energy = models.FloatField()
    carbohydrates = models.FloatField()
    fat = models.FloatField()
    proteins = models.FloatField()
    # Я начал работать

    def __str__(self):
        return f'{self.name}'


class FoodserviceRoles(models.TextChoices):
    WORKER = 'worker', 'Worker'
    ADMIN = 'admin', 'Admin'


class FoodserviceWorker(models.Model):
    foodservice = models.ForeignKey(Foodservice, on_delete=models.CASCADE)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=FoodserviceRoles.choices)

    class Meta:
        unique_together = ('foodservice', 'worker')

    def __str__(self):
        return f'{self.worker.email} - {self.foodservice.title} - {self.role}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    count = models.IntegerField()


class FavoriteDish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'dish')

    def __str__(self):
        return f'{self.user.username} - {self.dish.id}'


class FavoriteFoodservice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foodservice = models.ForeignKey(Foodservice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'foodservice')

    def __str__(self):
        return f'{self.user.username} - {self.foodservice.title}'


class Menu(models.Model):
    date = models.DateField(auto_now_add=True, blank=True)
    def __str__(self):
        return f'{self.date}'
    
class MenuDetails(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} {self.dish}'
