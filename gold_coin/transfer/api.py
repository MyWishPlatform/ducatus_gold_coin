import datetime

from gold_coin.transfer.models import DucatusTransfer, ErcTransfer
from gold_coin.litecoin_rpc import DucatuscoreInterface
from gold_coin.parity_interface import ParityInterface
from gold_coin.consts import DUC_USD_RATE, DECIMALS


class TransferMaker:
    @classmethod
    def transfer(cls, coin):
        cls.duc_transfer(coin)
        cls.erc_transfer(coin)

    @staticmethod
    def duc_transfer(coin):
        rpc = DucatuscoreInterface()
        amount = (coin.token_type * coin.gold_price * coin.duc_value / DUC_USD_RATE) * DECIMALS['DUC']
        address = coin.ducatus_address
        tx_hash = rpc.node_transfer(address, amount)

        transfer_info = DucatusTransfer()
        transfer_info.user = coin
        transfer_info.amount = amount
        transfer_info.tx_hash = tx_hash
        transfer_info.save()

    @staticmethod
    def erc_transfer(coin):
        parity = ParityInterface()
        amount = 1
        address = coin.ducatusx_address
        coin_weight = coin.token_type
        tx_hash, token_id = parity.transfer(address, coin_weight, coin.user_id)

        coin.mint_date = str(datetime.datetime.now())
        coin.token_id = token_id
        coin.save()

        transfer_info = ErcTransfer()
        transfer_info.user = coin
        transfer_info.amount = amount
        transfer_info.tx_hash = tx_hash
        transfer_info.save()


class TransferReceiver:
    @staticmethod
    def parse_duc_message(message):
        tx_hash = message.get('txHash')
        transfer_info = DucatusTransfer.objects.get(tx_hash=tx_hash)
        transfer_info.transfer_status = 'CONFIRMED'
        transfer_info.save()

    @staticmethod
    def parse_erc_message(message):
        tx_hash = message.get('txHash')
        transfer_info = ErcTransfer.objects.get(tx_hash=tx_hash)
        transfer_info.transfer_status = 'CONFIRMED'
        transfer_info.save()
