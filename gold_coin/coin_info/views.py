from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from gold_coin.coin_info.models import TokenInfo
from gold_coin.coin_info.serializers import TokenInfoSerializer
from gold_coin.transfer.api import TransferMaker


class CoinRequest(APIView):

    @swagger_auto_schema(
        operation_description='get coin info using unique public_code',
        manual_parameters=[
            openapi.Parameter('public_code', openapi.IN_QUERY, description="required param", type=openapi.TYPE_STRING)
        ],
        responses={200: TokenInfoSerializer()},
    )
    def get(self, request):
        public_code = TokenInfoSerializer.key_format(request.query_params['public_code'])
        coin = TokenInfo.objects.filter(public_code=public_code).first()
        if coin:
            return Response(TokenInfoSerializer().to_representation(coin))
        raise NotFound('coin with public_code={public_code} not exist'.format(public_code=public_code))

    @swagger_auto_schema(
        operation_description="coin register for raffle",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['secret_code', 'ducatus_address', 'ducatusx_address'],
            properties={
                'secret_code': openapi.Schema(type=openapi.TYPE_STRING),
                'ducatus_address': openapi.Schema(type=openapi.TYPE_STRING),
                'ducatusx_address': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        responses={200: TokenInfoSerializer()},
    )
    def post(self, request):
        print('request data', request.data, flush=True)
        serializer = TokenInfoSerializer()
        validated_data = serializer.validate(request.data)
        coin = TokenInfo.objects.get(secret_code=validated_data['secret_code'])
        TokenInfoSerializer().update(coin, validated_data)
        TransferMaker.transfer(coin)
        return Response(TokenInfoSerializer().to_representation(coin))
