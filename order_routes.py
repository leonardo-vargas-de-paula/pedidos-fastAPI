from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/pedido")
async def get_orders():
    return {"message": "List of orders"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(get_session)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Order created successfully id = {novo_pedido.id}"}
