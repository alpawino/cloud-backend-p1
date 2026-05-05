from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="History Aggregator Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs internas de los otros microservicios (dentro de Docker usan el nombre del servicio)
USERS_URL = os.getenv("USERS_URL", "http://users-api:8000")
ORDERS_URL = os.getenv("ORDERS_URL", "http://orders-service:8083/api")


@app.get("/")
def root():
    return {"message": "History Aggregator Service 🚀"}


@app.get("/history/{user_id}")
async def get_full_history(user_id: int):
    """
    Consume los microservicios de Usuarios y Órdenes,
    combina los datos y devuelve un resumen completo.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Obtener datos del usuario
        try:
            user_resp = await client.get(f"{USERS_URL}/users/{user_id}")
            user_data = user_resp.json() if user_resp.status_code == 200 else None
        except Exception:
            user_data = None

        # 2. Obtener órdenes del usuario
        try:
            orders_resp = await client.get(f"{ORDERS_URL}/orders", params={"userId": user_id})
            orders_data = orders_resp.json() if orders_resp.status_code == 200 else []
        except Exception:
            orders_data = []

    if not user_data:
        raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")

    # 3. Calcular resumen
    total_orders = len(orders_data)
    total_spent = sum(float(o.get("total", 0)) for o in orders_data)

    return {
        "user": user_data,
        "orders": orders_data,
        "summary": {
            "total_orders": total_orders,
            "total_spent": round(total_spent, 2),
            "average_order": round(total_spent / total_orders, 2) if total_orders > 0 else 0
        }
    }


@app.get("/history/{user_id}/summary")
async def get_history_summary(user_id: int):
    """Devuelve solo el resumen sin los detalles de las órdenes."""
    full = await get_full_history(user_id)
    return {
        "user_id": user_id,
        "name": full["user"].get("name", ""),
        **full["summary"]
    }
