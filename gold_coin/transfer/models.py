from django.db import models

from gold_coin.coin_info.models import TokenInfo
from gold_coin.consts import MAX_DIGITS


class TransferInfo(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(TokenInfo, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=0)
    tx_hash = models.CharField(max_length=100)
    transfer_status = models.CharField(max_length=50, default='WAIT_FOR_CONFIRM')


class DucatusTransfer(TransferInfo):
    pass


class ErcTransfer(TransferInfo):
    pass
