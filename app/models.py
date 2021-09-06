from django.db import models
from datetime import date, datetime
import re

# Create your models here.

class UserManager(models.Manager):

    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['nombre']) < 2:
            errors['firstname_len'] = "Nombre debe tener al menos 2 caracteres de largo"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Correo invalido"

        if not SOLO_LETRAS.match(postData['nombre']):
            errors['solo_letras'] = "Solo letras en nombre por favor"

        if len(postData['password']) < 4:
            errors['password'] = "Contraseña debe tener al menos 8 caracteres."

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "Contraseña y confirmar contraseña no son iguales. "

        
        return errors


class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=70)
    rol = models.CharField(max_length=10, default = 'NORMAL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"


class Message(models.Model):
    usuariom = models.ForeignKey(User, related_name="usuarioms", on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return f"{self.id}"

class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comentarios', on_delete = models.CASCADE)
    mensajec = models.ForeignKey(Message, related_name="comentario_mensaje", on_delete=models.CASCADE)
    comentario = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

