# Wallet-Endpoint

## Тестовое задание (SOLID Version)

Тех. задание: [Ссылка на тестовое задание](https://docs.google.com/document/d/1hEnCQnhljJ-pAwg7coi31J_3A05ctPcysIdkIuHXRqs/edit?tab=t.0#heading=h.pxfv6y3ftfw9)

##

Скачивание:

```
git clone https://github.com/DanielBarutov/Wallet-Endpoint.git
cd Wallet-Endpoint

```

Запуск:

```
docker compose up -d --build
```

Ручной запуск тестирования (при запущенном контейнере):

```
docker compose exec wallet-endpoint pytest
```

При запуске тестирования создаются тестовые данные в тестовой базе данных(SQLite для тестов).

Swagger:

```
http://localhost:8000/docs
```
