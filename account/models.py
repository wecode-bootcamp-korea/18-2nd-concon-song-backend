from django.db import models
from product.models import ProductSize, Product


class Account(models.Model):
    email    = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    name     = models.CharField(max_length=50)

    class Meta:
        db_table = 'accounts'


class WishList(models.Model):
    account      = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlists'


class Review(models.Model):
    account    = models.ForeignKey(Account, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating     = models.IntegerField(default=0)
    content    = models.TextField()
    image      = models.CharField(max_length=400) 
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'reviews'
