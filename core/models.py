from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20)
    fio = models.CharField(max_length=200)

class Application(models.Model):
    STATUS = [
        ('Новая', 'Новая'),
        ('Идет обучение', 'Идет обучение'),
        ('Обучение завершено', 'Обучение завершено'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=200)
    desired_date = models.DateField()
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS, default='Новая')
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.TextField(blank=True, null=True)