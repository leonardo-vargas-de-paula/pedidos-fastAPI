from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.dependencies import get_session, verificar_token
from app.models.models import Usuario
from app.main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.schemas.schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao
    dic_info = {
        "sub": str(id_usuario),
        "exp": data_expiracao
    }
    token = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return token

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


@auth_router.get("/")
async def home():
    """
    docstring...
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


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, timedelta(days=7))
        return {
            "access_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

#authorize padrao do fastapi
@auth_router.post("/login-form")
async def login_form(formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    usuario = autenticar_usuario(formulario.username, formulario.password, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        acess_token = criar_token(usuario.id)
        
        return {
            "access_token": acess_token,
            "token_type": "Bearer"
        }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario)
    return{
        "access_token": acess_token,
        "token_type": "Bearer"
    }