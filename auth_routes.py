from fastapi import APIRouter, Depends
from dependencies import get_session
from models import Usuario
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """

    rota docstring...
    
    """
    return {"message": "Authentication successful"}

@auth_router.post("/signup")
async def signup(nome:str,email: str, senha: str, session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        return {"message": "Usuário já existe"}
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"message": "Usuário cadastrado com sucesso"}
    
    return {"email": email, "senha": senha}