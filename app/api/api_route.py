
from enum import Enum
from fastapi import APIRouter, HTTPException
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from app.db.db import get_db
from fastapi import Depends
from pydantic import BaseModel
from app.model.wallet import Wallet
import uuid

# Pydantic models


class WalletCreate(BaseModel):
    balance: float


class WalletRead(BaseModel):
    wallet_uuid: str
    balance: float


class WalletsRead(BaseModel):
    wallets: list[WalletRead]


class OperationType(str, Enum):
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"

# Routes


router = APIRouter(prefix="/api/v1")


@router.get("/wallets")
def get_wallets(db: Session = Depends(get_db)):
    wallet = db.execute(select(Wallet)).scalars().all()
    if wallet != []:
        result = [WalletRead(wallet_uuid=wallet.wallet_uuid,
                             balance=wallet.balance) for wallet in wallet]
        return result
    else:
        raise HTTPException(404, "Wallets не обнаружено!")


@router.post("/wallets/")
def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    new_wallet = Wallet(wallet_uuid=str(uuid.uuid4()), balance=wallet.balance)
    try:
        db.add(new_wallet)
        db.commit()
        return {"message": "Wallet успешно создан"}
    except Exception as e:
        raise HTTPException(500, f"Wallet не создан! Ошибка: {e}")


@router.get("/wallet/{wallet_uuid}")
def get_wallet_balance(wallet_uuid: str, db: Session = Depends(get_db)):
    wallet = db.execute(select(Wallet).where(
        Wallet.wallet_uuid == wallet_uuid)).scalar()
    if wallet != None:
        return {"balance": wallet.balance}
    else:
        raise HTTPException(404, "Wallet по этому UUID не обнаружен!")


@router.post("/wallets/{wallet_uuid}/operation")
def create_operation(wallet_uuid: str, operation_type: OperationType, amount: float, db: Session = Depends(get_db)):
    wallet = db.execute(select(Wallet).where(
        Wallet.wallet_uuid == wallet_uuid)).scalar()
    if not wallet:
        raise HTTPException(404, "Waalet not found")
    if operation_type == "DEPOSIT":
        wallet.balance = Wallet.balance + amount
    if operation_type == "WITHDRAW":
        wallet.balance = Wallet.balance - amount
    try:
        db.commit()
        db.refresh(wallet)
        return {"message": f"Баланс успешно {'пополнен' if operation_type == 'DEPOSIT' else 'списан'} на {amount} у.е.. Текущий баланс: {wallet.balance}"}
    except Exception as e:
        raise HTTPException(
            500, f"Пополнение баланса не произошло! Ошибка: {e}")
