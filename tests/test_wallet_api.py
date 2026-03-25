from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.db import get_db
from app.main import app
from app.model.base import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_wallet.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_wallet():
    start_balance = 100.0
    response = client.post(
        f"/api/v1/wallets/?start_balance={start_balance}")

    assert response.status_code == 200
    uid = response.json()["uuid_wallet"]
    assert response.json()[
        "message"] == f"Wallet c UUID: {uid[0]} и стартовым балансом: {start_balance}р. успешно создан"


def test_get_wallets_returns_created_wallet():
    create_response = client.post("/api/v1/wallets/?start_balance=150")
    assert create_response.status_code == 200
    uid = create_response.json()["uuid_wallet"]

    response = client.get("/api/v1/wallets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["wallet_uuid"] == uid[0]
    assert data[0]["balance"] == 150.0


def test_get_wallet_balance():
    client.post("/api/v1/wallets/?start_balance=75")
    wallets = client.get("/api/v1/wallets").json()
    wallet_uuid = wallets[0]["wallet_uuid"]

    response = client.get(f"/api/v1/wallet/{wallet_uuid}")

    assert response.status_code == 200
    assert response.json() == {"balance": 75.0}


def test_create_operation_deposit():
    client.post("/api/v1/wallets/?start_balance=50")
    wallets = client.get("/api/v1/wallets").json()
    wallet_uuid = wallets[0]["wallet_uuid"]

    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        params={"operation_type": "DEPOSIT", "amount": 25.0},
    )

    assert response.status_code == 200
    balance_response = client.get(f"/api/v1/wallet/{wallet_uuid}")
    assert balance_response.json() == {"balance": 75.0}


def test_create_operation_withdraw():
    client.post("/api/v1/wallets/?start_balance=50")
    wallets = client.get("/api/v1/wallets").json()
    wallet_uuid = wallets[0]["wallet_uuid"]

    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        params={"operation_type": "WITHDRAW", "amount": 20.0},
    )

    assert response.status_code == 200
    balance_response = client.get(f"/api/v1/wallet/{wallet_uuid}")
    assert balance_response.json() == {"balance": 30.0}


def test_create_operation_returns_404_for_missing_wallet():
    wallet_uuid = "unknown_wallet"
    response = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        params={"operation_type": "DEPOSIT", "amount": 10.0},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Кошелек с UUID: {wallet_uuid} не найден!"}


def test_create_operation_twice_res():
    client.post("/api/v1/wallets/?start_balance=50")
    wallets = client.get("/api/v1/wallets").json()
    wallet_uuid = wallets[0]["wallet_uuid"]
    attemp = 0
    while attemp != 5:
        response = client.post(
            f"/api/v1/wallets/{wallet_uuid}/operation",
            params={"operation_type": "WITHDRAW", "amount": 5.0},
        )
        attemp += 1
        assert response.status_code == 200
    balance_response = client.get(f"/api/v1/wallet/{wallet_uuid}")
    assert balance_response.json() == {"balance": 25.0}
