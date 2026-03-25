from typing import Callable
from app.shemas.wallet_shemas import OperationType, WalletRead, WalletCreate
from app.exceptions import WalletNotFound, NegativeBalanceError, OperationBalanceError
from app.model.wallet import Wallet
from app.repository.wallet_repository import (
    list_wallets, add_wallet, get_wallet, add_balance, remove_balance)
import uuid


def get_wallets_service(db: Callable) -> dict:
    wallet = list_wallets(db)
    result = [WalletRead(wallet_uuid=wallet.wallet_uuid,
                         balance=wallet.balance) for wallet in wallet]
    if result == []:
        raise WalletNotFound
    return result


def create_wallets_service(start_balance: WalletCreate, db: Callable) -> dict:
    if start_balance < 0:
        raise NegativeBalanceError
    uid = str(uuid.uuid4())
    new_wallet = Wallet(wallet_uuid=uid, balance=start_balance)
    add_wallet(new_wallet, db)
    return {"message": f"Wallet c UUID: {uid} и стартовым балансом: {start_balance}р. успешно создан",
            "uuid_wallet": uid,
            "start_balance": start_balance
            }


def check_balance_service(wallet_uuid: str, db: Callable) -> dict:
    wallet = get_wallet(wallet_uuid, db)
    if wallet == None:
        raise WalletNotFound
    return {"balance": wallet.balance}


def create_operation_service(wallet_uuid: str, operation_type: OperationType, amount, db: Callable) -> dict:
    wallet = get_wallet(wallet_uuid, db)
    if wallet == None:
        raise WalletNotFound
    if operation_type == "DEPOSIT":
        if amount <= 0:
            raise OperationBalanceError
        add_balance(wallet, amount, db)
    if operation_type == "WITHDRAW":
        if wallet.balance <= 0:
            raise OperationBalanceError
        if wallet.balance < amount:
            raise OperationBalanceError
        remove_balance(wallet, amount, db)
    return {"message": f"Баланс успешно {'пополнен' if operation_type == 'DEPOSIT' else 'списан'} на {amount} у.е.. Текущий баланс: {wallet.balance}"}
