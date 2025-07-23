from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Body
from pydantic import UUID4

from api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaOutSummary
from api.atleta.models import AtletaModel
from api.categorias.models import CategoriaModel
from api.categorias.schemas import CategoriaOut
from api.centro_treinamento.models import CentroTreinamentoModel
from api.contrib.dependencies import DatabaseDependency
from datetime import datetime, timezone
from sqlalchemy.future import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    categoria_name = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_name))).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_name} não foi encontrada.'
        )
    
    centro_treinamento_nome = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first()
    
    if not centro_treinamento_nome:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(timezone.utc),**atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento_nome.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}'
        )

    return atleta_out

@router.get(
    '/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOutSummary],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOutSummary]:
    atletas: list[AtletaOutSummary] = (await db_session.execute(select(AtletaModel))).scalars().all()
    
    return [AtletaOutSummary.model_validate(atleta) for atleta in atletas]

# GET BY ID
@router.get(
    '/{id}',
    summary='Consultar uma atleta pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado(a) no id: {id}.'
        )
    
    return atleta

# GET BY NAME AND CPF
@router.get(
    '/{name}/{cpf}',
    summary='Consultar uma atleta pelo Nome e CPF',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(name: str = None, cpf: str = None, db_session: DatabaseDependency = None) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(nome=name, cpf=cpf))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado(a) com nome: {name} e cpf: {cpf}.'
        )
    
    return atleta

# Patch Para editar um atleta dinamicamente
@router.patch(
    '/{id}',
    summary='Editar um atleta pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado(a) no id: {id}.'
        )
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    
    await db_session.commit()
    await db_session.refresh(atleta)
    
    return atleta

# DELETE Atleta BY ID
@router.delete(
    '/{id}',
    summary='Delete um atleta pelo ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado(a) no id: {id}.'
        )
    
    await db_session.delete(atleta)
    await db_session.commit()