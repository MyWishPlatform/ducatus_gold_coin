from django.conf.urls import url

from gold_coin.coin_info.views import CoinRequest

urlpatterns = [
    url(r'^$', CoinRequest.as_view(), name='coin-info-request'),
]
