## Endpoints base

- `POST /api/orders`
- `GET /api/orders`
- `GET /api/orders/{id}`

## Levantar PostgreSQL

```bash
docker compose up -d
```

Eso crea:

- Base de datos: `orders_db`
- Usuario: `postgres`
- Password: `postgres`
- Puerto: `5432`

## Ejecutar la app

```bash
mvn spring-boot:run
```

La API queda en:

- `http://localhost:8083/api/orders`

## Ejecutar todo con un solo comando

En PowerShell:

```powershell
.\run-orders-service.ps1
```

Ese script:

- levanta PostgreSQL con Docker
- espera a que la base este disponible
- arranca el microservicio de ordenes

## Ejemplo de creacion de pedido

```json
{
  "userId": 1,
  "items": [
    {
      "productId": 101,
      "quantity": 2,
      "unitPrice": 49.99
    },
    {
      "productId": 205,
      "quantity": 1,
      "unitPrice": 19.90
    }
  ]
}
```

## Probar rapido en PowerShell

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8083/api/orders" `
  -ContentType "application/json" `
  -Body '{
    "userId": 1,
    "items": [
      {
        "productId": 101,
        "quantity": 2,
        "unitPrice": 49.99
      }
    ]
  }'
```
