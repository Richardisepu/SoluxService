from decimal import Decimal
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator

from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
