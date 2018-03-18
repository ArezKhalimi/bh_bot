from django.db import models


class ProductComposition(models.Model):
    proteins = models.IntegerField()
    fat = models.DecimalField(max_digits=10, decimal_places=2)
    carbohydrate = models.DecimalField(max_digits=10, decimal_places=2)
    calories = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


class Product(ProductComposition):
    name = models.CharField(max_length=255)
