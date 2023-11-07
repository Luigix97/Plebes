from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from django.contrib.auth.hashers import make_password



# Create your models here.

class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(limit_value=6)])
    nombre = models.CharField(max_length=50)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(limit_value=8)])
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    
    class Rol(models.TextChoices):
        ADMIN = 'Admin', 'Administrador'
        INTENDENCIA = 'Intendente', 'Intendencia'
    rol = models.CharField(max_length=12, choices=Rol.choices)
    edificio = models.CharField(max_length=50, blank=True, null=True)
    piso = models.IntegerField(blank=True, null=True)
    
    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return password == self.password

    def __str__(self):
        return self.username