from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from gold_coin.coin_info.models import TokenInfo
from gold_coin.coin_info.serializers import TokenInfoSerializer


class CoinRequest(APIView):

    @swagger_auto_schema(
        operation_description='get coin info using unique user_id',
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)
        ],
        responses={200: TokenInfoSerializer()},
    )
    def get(self, request):
        user_id = request.query_params['user_id']
        coin = TokenInfo.objects.filter(user_id=user_id, is_active=True).first()
        if coin:
            return Response(TokenInfoSerializer().to_representation(coin))
        raise ValidationError('user with id={user_id} not exist'.format(user_id=user_id))

    @swagger_auto_schema(
        operation_description="coin register for raffle",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'ducatus_address', 'ducatusx_address'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING),
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
        coin = TokenInfo.objects.get(user_id=validated_data['user_id'])
        TokenInfoSerializer().update(coin, validated_data)
        return Response(TokenInfoSerializer().to_representation(coin))
