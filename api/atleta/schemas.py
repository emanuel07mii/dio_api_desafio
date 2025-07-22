from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from api.categorias.schemas import CategoriaIn
from api.centro_treinamento.schemas import CentroTreinamentoAtleta
from api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", example=75.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", example=1.75)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do Atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de Treinamento do Atleta")]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do atleta", example="João", max_length=50)]
    # cpf: Annotated[Optional[str], Field(None, description="CPF do atleta", example="12345678900", max_length=11)]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", example=25)]
    peso: Annotated[Optional[PositiveFloat], Field(None, description="Peso do atleta em kg", example=75.5)]
    altura: Annotated[Optional[PositiveFloat], Field(None, description="Altura do atleta em metros", example=1.75)]
    # sexo: Annotated[Optional[str], Field(None, description="Sexo do atleta", example="M", max_length=1)]
    # categoria: Annotated[Optional[CategoriaIn], Field(None, description="Categoria do Atleta")]
    # centro_treinamento: Annotated[Optional[CentroTreinamentoAtleta], Field(None, description="Centro de Treinamento do Atleta")]