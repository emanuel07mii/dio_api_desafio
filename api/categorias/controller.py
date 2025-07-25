from uuid import uuid4
from fastapi import Body, APIRouter, status
from pydantic import UUID4

from api.categorias.schemas import CategoriaIn
from api.categorias.schemas import CategoriaOut
from api.categorias.models import CategoriaModel
from api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from fastapi import HTTPException
router = APIRouter()
from fastapi_pagination import Page, paginate, Params
from fastapi import Depends
from fastapi_pagination.utils import disable_installed_extensions_check

@router.post(
    '/',
    summary='Criar uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    
    try:
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())

        db_session.add(categoria_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe uma categoria cadastrada com o nome: {categoria_in.nome}'
        )
    
    return categoria_out

@router.get(
    '/',
    summary='Consultar todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoriaOut],
)
async def query(db_session: DatabaseDependency, params: Params = Depends()) -> Page[CategoriaOut]:
    categorias = (await db_session.execute(select(CategoriaModel).order_by(CategoriaModel.nome))).scalars().all()
    
    disable_installed_extensions_check()
    return paginate(categorias, params)

@router.get(
    '/{id}',
    summary='Consultar uma categoria pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria não encontrada no id: {id}.'
        )
    
    return categoria