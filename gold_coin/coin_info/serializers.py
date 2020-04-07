from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from gold_coin.coin_info.models import TokenInfo
from gold_coin.transfer.models import DucatusTransfer, ErcTransfer


class TokenInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenInfo
        fields = ('public_code', 'ducatus_address', 'ducatusx_address', 'token_type', 'is_active', 'mint_date',
                  'country', 'certified_assayer', 'purchase_date', 'token_id', 'duc_value', 'gold_price')

    def validate(self, data):
        public_code = data['public_code']
        coin = TokenInfo.objects.filter(public_code=public_code).first()
        if not coin:
            raise PermissionDenied(
                detail='user with public_code={public_code} not exist'.format(public_code=public_code))
        if coin.is_active:
            raise PermissionDenied(
                detail='user with public_code={public_code} has already registered'.format(public_code=public_code))
        data['ducatusx_address'] = data['ducatusx_address'].lower()
        data['is_active'] = True
        return data

    def to_representation(self, instance):
        repr_instance = super().to_representation(instance)
        duc_transfer = DucatusTransfer.objects.get(user=instance)
        erc_transfer = ErcTransfer.objects.get(user=instance)
        repr_instance.update({
            'duc_transfer_amount': duc_transfer.amount,
            'duc_transfer_tx_hash': duc_transfer.tx_hash,
            'duc_transfer_status': duc_transfer.transfer_status,
            'erc_transfer_amount': erc_transfer.amount,
            'erc_transfer_tx_hash': erc_transfer.tx_hash,
            'erc_transfer_status': erc_transfer.transfer_status
        })

        return repr_instance
