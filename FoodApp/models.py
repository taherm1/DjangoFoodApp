from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ready-to-eat', 'Ready to Eat'),
        ('ready-to-cook', 'Ready to Cook'),
        ('ready-to-drink', 'Ready to Drink')
    ]

    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.CharField(max_length=255)

    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.CharField(max_length=255)
    status = models.IntegerField(
        default=0, choices=[(0, 'PENDING'), (1, 'DISPATCHED'), (2, 'COMPLETE')])
    date = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.product.price
