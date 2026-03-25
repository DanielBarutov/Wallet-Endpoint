
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from fastapi import Depends

from app.shemas.wallet_shemas import OperationType
from app.exceptions import WalletNotFound, NegativeBalanceError, OperationBalanceError
from app.service.wallet_service import (
    check_balance_service,
    create_wallets_service,
    get_wallets_service,
    create_operation_service
)

# Routes
router = APIRouter(prefix="/api/v1")


@router.get("/wallets")
def get_wallets(db: Session = Depends(get_db)):
    try:
        return get_wallets_service(db)
    except WalletNotFound:
        raise HTTPException(404, "Wallets не обнаружено!")
    except Exception as e:
        raise HTTPException(500, f"Неизвестная ошибка: {e}")


@router.post("/wallets/")
def create_wallet(start_balance: float, db: Session = Depends(get_db)):
    try:
        return create_wallets_service(start_balance, db)
    except NegativeBalanceError:
        raise HTTPException(400, "Начальный баланс не может быть ниже нуля!")
    except Exception as e:
        raise HTTPException(500, f"Неизвестная ошибка: {e}")


@router.get("/wallet/{wallet_uuid}")
def get_wallet_balance(wallet_uuid: str, db: Session = Depends(get_db)):
    try:
        return check_balance_service(wallet_uuid, db)
    except WalletNotFound:
        raise HTTPException(404, "Wallet по этому UUID не обнаружен!")
    except Exception as e:
        raise HTTPException(500, f"Неизвестная ошибка: {e}")


@router.post("/wallets/{wallet_uuid}/operation")
def create_operation(wallet_uuid: str, operation_type: OperationType, amount: float, db: Session = Depends(get_db)):
    try:
        return create_operation_service(wallet_uuid, operation_type, amount, db)
    except OperationBalanceError:
        raise HTTPException(
            400, "Неверная операция с балансом, возможно вывод больше чем баланс, или пополнение отрицательной суммой")
    except WalletNotFound:
        raise HTTPException(404, f"Кошелек с UUID: {wallet_uuid} не найден!")
    except Exception as e:
        raise HTTPException(
            500, f"Пополнение баланса не произошло! Ошибка: {e}")
