from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from gold_coin.coin_info.models import TokenInfo
from gold_coin.transfer.models import DucatusTransfer, ErcTransfer


class TokenInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenInfo
        fields = ('public_code', 'ducatus_address', 'ducatusx_address', 'token_type', 'is_active', 'mint_date',
                  'country', 'certified_assayer', 'purchase_date', 'token_id', 'duc_value', 'gold_price',
                  'production_date')

    def validate(self, data):
        secret_code = data['secret_code']
        coin = TokenInfo.objects.filter(secret_code=secret_code).first()
        if not coin:
            raise ValidationError(
                detail='coin with secret_code={secret_code} not exist'.format(secret_code=secret_code))
        if coin.is_active:
            raise PermissionDenied(
                detail='coin with secret_code={secret_code} has already registered'.format(secret_code=secret_code))
        data['ducatusx_address'] = data['ducatusx_address'].lower()
        data['is_active'] = True
        return data

    def to_representation(self, instance):
        repr_instance = super().to_representation(instance)
        if instance.is_active:
            duc_transfer = DucatusTransfer.objects.filter(user=instance).first()
            erc_transfer = ErcTransfer.objects.filter(user=instance).first()
            if duc_transfer:
                repr_instance.update({
                    'duc_transfer_amount': duc_transfer.amount,
                    'duc_transfer_tx_hash': duc_transfer.tx_hash,
                    'duc_transfer_status': duc_transfer.transfer_status
                })
            if erc_transfer:
                repr_instance.update({
                    'erc_transfer_amount': erc_transfer.amount,
                    'erc_transfer_tx_hash': erc_transfer.tx_hash,
                    'erc_transfer_status': erc_transfer.transfer_status
                })

        return repr_instance
