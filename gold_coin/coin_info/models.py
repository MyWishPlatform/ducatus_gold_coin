from django.db import models


class TokenInfo(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    ducatus_address = models.CharField(max_length=50, null=True, default=None)
    ducatusx_address = models.CharField(max_length=50, null=True, default=None)
    token_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
