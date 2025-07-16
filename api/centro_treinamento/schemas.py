from pydantic import UUID4, Field
from typing_extensions import Annotated
from api.contrib.schemas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de Treinamento", example="CT King", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de Treinamento", example="Rua das X, Quadra 2", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de Treinamento", example="João Silva", max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de Treinamento", example="CT King", max_length=20)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="ID do centro de Treinamento")]