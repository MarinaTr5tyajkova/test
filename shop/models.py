from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)

class Product(models.Model):
    name = models.CharField(max_length=255)  # Название товара
    description = models.TextField()          # Описание товара
    image = models.ImageField(upload_to='products/')  # Изображение товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара
    created_at = models.DateTimeField(auto_now_add=True)  # Дата добавления товара

    def __str__(self):
        return self.name  # Возвращает название товара при выводе объекта



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ссылаемся на кастомную модель пользователя
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связываем заказ с продуктом
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания заказа

    def __str__(self):
        return f"Order {self.id} by {self.user.username} for {self.product.name}"