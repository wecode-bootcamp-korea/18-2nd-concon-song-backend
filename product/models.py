import uuid

from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'collections'

class Product(models.Model):
    collection       = models.ForeignKey('product.Collection', on_delete=models.CASCADE)
    name             = models.CharField(max_length=100)
    price            = models.DecimalField(max_digits=18, decimal_places=0)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    stock            = models.IntegerField(default=10)
    main_image       = models.URLField(max_length=500)
    item_code        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    color            = models.CharField(max_length=100)

    class Meta:
        db_table = 'products'


class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'colors'


class Size(models.Model):
    name    = models.CharField(max_length=100)
    product = models.ManyToManyField('product.Product', through='ProductSize')

    class Meta:
        db_table = 'sizes'


class ProductSize(models.Model):
    size    = models.ForeignKey('product.Size', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_sizes'


class ProductDetail(models.Model):
    product      = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    description  = models.TextField()
    introduction = models.CharField(max_length=100)
    url          = models.URLField(max_length=500)

    class Meta:
        db_table = 'product_detail'