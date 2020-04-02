from gold_coin.transfer.models import DucatusTransfer, ErcTransfer
from gold_coin.litecoin_rpc import DucatuscoreInterface
from gold_coin.parity_interface import ParityInterface
from gold_coin.consts import DUC_AMOUNT


class TransferMaker:
    @classmethod
    def transfer(cls, coin):
        cls.duc_transfer(coin)
        # cls.erc_transfer(coin)

    @staticmethod
    def duc_transfer(coin):
        rpc = DucatuscoreInterface()
        amount = DUC_AMOUNT[coin.token_type]
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
        coin_weight = int(coin.token_type.split('GRAM')[0])
        tx_hash = parity.transfer(address, coin_weight, coin.user_id)

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
