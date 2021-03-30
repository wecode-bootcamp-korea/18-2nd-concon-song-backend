from django.db import models

from product.models import Product, ProductSize
from account.models  import Account


class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'statuses'

class Order(models.Model):
    status       = models.ForeignKey(Status, on_delete=models.CASCADE)
    account      = models.ForeignKey(Account, on_delete=models.CASCADE)
    product      = models.ManyToManyField(ProductSize, through='Cart')

    class Meta:
        db_table = 'orders'


class Cart(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_size    = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity        = models.IntegerField()

    class Meta:
        db_table = 'carts'