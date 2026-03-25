from typing import Callable
from sqlalchemy import select
from app.model.wallet import Wallet
from app.exceptions import DatabaseError


def list_wallets(db: Callable):
    try:
        wallet = db.execute(select(Wallet)).scalars().all()
        return wallet
    except Exception:
        raise DatabaseError


def add_wallet(new_wallet: Wallet, db: Callable) -> None:
    try:
        db.add(new_wallet)
        db.commit()
    except Exception:
        raise DatabaseError


def get_wallet(wallet_uuid: str, db: Callable) -> None:
    try:
        wallet = db.execute(select(Wallet).where(
            Wallet.wallet_uuid == wallet_uuid)).scalar()
        return wallet
    except Exception:
        raise DatabaseError


def add_balance(wallet: Wallet, amount: float, db: Callable) -> None:
    wallet.balance = Wallet.balance + amount
    try:
        db.commit()
        db.refresh(wallet)
    except Exception:
        raise DatabaseError


def remove_balance(wallet: Wallet, amount: float, db: Callable) -> None:
    wallet.balance = Wallet.balance - amount
    try:
        db.commit()
        db.refresh(wallet)
    except Exception:
        raise DatabaseError
