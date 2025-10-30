from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.dependencies import get_session, verificar_token
from app.schemas.schemas import PedidoSchema, ItemPedidoSchema
from app.models.models import Pedido, Usuario, ItemPedido

order_router = APIRouter(
    prefix="/orders", tags=["orders"], dependencies=[Depends(verificar_token)])


@order_router.get("/")
async def get_orders():
    return {"message": "Pedidos"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(get_session)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Order created successfully id = {novo_pedido.id}"}


@order_router.put("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(get_session), usuario: Usuario = Depends(verificar_token)):

    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=401, detail="Usuario nao autorizado a cancelar este pedido")

    pedido.status = "CANCELADO"
    session.commit()

    return {
        "message": f"Pedido {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }


@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(get_session), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Usuario nao autorizado")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }


@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(get_session),
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=401, detail="Usuario nao autorizado a adicionar item a este pedido")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho,
                             item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "message": f"Item adicionado ao pedido {pedido.id} com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }


@order_router.delete("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(get_session), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(
        ItemPedido.id == id_item_pedido).first()

    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item nao encontrado")
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuario nao autorizado")

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "message": f"Item removido do pedido {pedido.id} com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }

