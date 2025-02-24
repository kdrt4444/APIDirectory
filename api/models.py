from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='materials')
    code = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return self.name