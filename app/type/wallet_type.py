from pydantic import BaseModel
from enum import Enum


class WalletCreate(BaseModel):
    balance: float


class WalletRead(BaseModel):
    wallet_uuid: str
    balance: float


class OperationType(str, Enum):
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"
