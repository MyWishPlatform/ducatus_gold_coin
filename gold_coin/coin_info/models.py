from django.db import models


class TokenInfo(models.Model):
    secret_code = models.CharField(max_length=50, unique=True)
    public_code = models.CharField(max_length=50, unique=True)
    ducatus_address = models.CharField(max_length=50, null=True, default=None)
    ducatusx_address = models.CharField(max_length=50, null=True, default=None)
    token_type = models.IntegerField()
    is_active = models.BooleanField(default=False)
    mint_date = models.CharField(max_length=50, null=True, default=None)
    country = models.CharField(max_length=100)
    certified_assayer = models.CharField(max_length=100)
    purchase_date = models.CharField(max_length=50)
    token_id = models.IntegerField(null=True, default=None)
    duc_value = models.FloatField()
    gold_price = models.FloatField()
