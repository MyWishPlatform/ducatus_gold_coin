from django.db import models


class TokenInfo(models.Model):
    user_id = models.CharField(max_length=50)
    ducatus_address = models.CharField(max_length=50)
    ducatusx_address = models.CharField(max_length=50)
    token_type = models.CharField(max_length=50)
