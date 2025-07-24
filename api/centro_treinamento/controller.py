from uuid import uuid4
from fastapi import Body, APIRouter, status
from pydantic import UUID4

from api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from api.centro_treinamento.models import CentroTreinamentoModel
from api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from fastapi import HTTPException
from fastapi_pagination import Page, paginate, Params
from fastapi import Depends
from fastapi_pagination.utils import disable_installed_extensions_check

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo Centro de Treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    
    try:
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

        db_session.add(centro_treinamento_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um centro de treinamento com o nome: {centro_treinamento_in.nome}'
        )
    
    return centro_treinamento_out

@router.get(
    '/',
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=Page[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency, params: Params = Depends()) -> Page[CentroTreinamentoOut]:
    centros_treinamento_out = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    
    disable_installed_extensions_check()
    return paginate(centros_treinamento_out, params)

@router.get(
    '/{id}',
    summary='Consultar um Centro de Treinamento pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento_out: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de Treinamento não encontrado no id: {id}.'
        )
    
    return centro_treinamento_out