from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    order = models.CharField(max_length=200)
    order_date = models.DateField("Date")
    image = models.ImageField(upload_to='customers')

class Page(models.Model):
    counterload = models.IntegerField()