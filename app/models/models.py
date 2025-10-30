from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils import ChoiceType

db = create_engine("sqlite:///banco.db")

Base = declarative_base()

"""
Usuario
Pedido
itensPedido
...
"""

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    email = Column("email",String, unique=True,  nullable=False)
    nome = Column("nome",String, nullable=False)
    senha = Column("senha",String, nullable=False)
    ativo = Column("ativo",Boolean)
    admin = Column("admin",Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin
        self.ativo = ativo


class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = {
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO"),
    # }

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    status = Column("status",String, nullable=False)
    usuario = Column("usuario",Integer, ForeignKey("usuarios.id"))
    preco = Column("preco", Float)

    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0.0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


class ItemPedido(Base):
    __tablename__ = "item_Pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido