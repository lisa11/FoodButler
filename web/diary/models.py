from django.db import models

# Create your models here.

class Food(models.Model):
    name = models.Charfield(max_length=64)
    calories = models.Integerfield()


### curl -sD -O #image url here

    