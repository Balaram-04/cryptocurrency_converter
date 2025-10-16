# converter/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    from_currency = models.CharField(max_length=50)   # e.g., 'bitcoin'
    to_currency = models.CharField(max_length=20)     # e.g., 'usd' or 'ethereum'
    from_amount = models.FloatField()
    to_amount = models.FloatField()
    raw_rate = models.FloatField()

    def __str__(self):
        return f"{self.from_amount} {self.from_currency} -> {self.to_amount} {self.to_currency} at {self.raw_rate}"
