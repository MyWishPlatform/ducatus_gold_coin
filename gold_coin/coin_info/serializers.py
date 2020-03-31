from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from gold_coin.coin_info.models import TokenInfo


class TokenInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenInfo
        fields = ('user_id', 'ducatus_address', 'ducatusx_address', 'token_type', 'is_active')

    def validate(self, data):
        user_id = data['user_id']
        coin = TokenInfo.objects.filter(user_id=user_id).first()
        if not coin:
            raise PermissionDenied(detail='user with id={user_id} not exist'.format(user_id=user_id))
        if coin.is_active:
            raise PermissionDenied(detail='user with id={user_id} has already registered'.format(user_id=user_id))
        data['is_active'] = True
        return data
