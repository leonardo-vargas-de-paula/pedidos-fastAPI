from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from models import Usuario
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    rota docstring...
    """
    return {"message": "Authentication successful"}

@auth_router.post("/signup")
async def signup(usuario_schema: UsuarioSchema, session: Session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"message": "Usuário cadastrado com sucesso"}
    
    return {"email": email, "senha": senha}