from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.db import get_db
from fastapi import Depends
from app.model.wallet import Wallet

app = FastAPI()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    wallet = db.execute(text("SELECT * FROM wallet"))
    return wallet