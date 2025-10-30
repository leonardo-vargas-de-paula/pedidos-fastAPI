from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.dependencies.dependencies import get_session, verificar_token
from app.schemas.schemas import PedidoSchema, ItemPedidoSchema
from app.models.models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies = [Depends(verificar_token)])

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
    
    
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuario nao autorizado a cancelar este pedido")


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
    
order_router.post("pedido/adicionar-tem/{id_pedido}")
async def adicionar_item_pedido( id_pedido:int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(get_session), 
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuario nao autorizado a adicionar item a este pedido")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unitario, id_pedido)
    