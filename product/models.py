from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'collections'


class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'colors'


class Product(models.Model):
    collection       = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name             = models.CharField(max_length=100)
    price            = models.DecimalField(max_digits=18, decimal_places=0)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    color_id         = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'


class Size(models.Model):
    name    = models.CharField(max_length=100)
    product = models.ManyToManyField(Product, through='ProductSize')

    class Meta:
        db_table = 'sizes'


class ProductSize(models.Model):
    stock   = models.IntegerField(default=10)
    size    = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_sizes'


class ProductDetail(models.Model):
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    description  = models.TextField()
    introduction = models.CharField(max_length=100)

    class Meta:
        db_table = 'product_detail'


class Image(models.Model):
    url       = models.URLField(max_length=500)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

