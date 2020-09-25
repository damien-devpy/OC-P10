from django.contrib.auth.models import AbstractUser
from django.db import models
from products_app.models import Product


class User(AbstractUser):
    """Custom model of an User."""
    favorites = models.ManyToManyField(Product, db_table="favorite")

    def __str__(self):
        # If user has record his first and last name, display it.
        if bool(self.first_name and self.last_name):
            return f'{self.first_name} {self.last_name}'
        # Otherwise display it's username
        return f'{self.username}'
