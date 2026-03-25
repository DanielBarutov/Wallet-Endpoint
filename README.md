# Wallet-Endpoint

## Тестовое задание (SOLID Version)

Тех. задание: [Ссылка на тестовое задание](https://docs.google.com/document/d/1hEnCQnhljJ-pAwg7coi31J_3A05ctPcysIdkIuHXRqs/edit?tab=t.0#heading=h.pxfv6y3ftfw9)

##

Скачивание:

```bash
git clone https://github.com/DanielBarutov/Wallet-Endpoint.git
cd Wallet-Endpoint

```

Запуск:

```bash
docker compose up -d --build
```

Ручной запуск тестирования (при запущенном контейнере):

```bash
docker compose exec wallet-endpoint pytest
```

При запуске тестирования создаются тестовые данные в тестовой базе данных(SQLite для тестов).

Swagger:

```
http://localhost:8000/docs
```

> > **P.S.**
> >
> > > Сейчас в коде есть ошибка утечки исключений, для теста и более простого логирования это не учитывается также как и отсутствия .env в gitignore

> > > Логичнее было бы выводить просто 500, без "e", а сам "e" и другие классы от Exception логировать. (Сделать все через внешний handler)

> > > Таким образом получили бы чистый ручки в API и избавились бы от утечки данных.
