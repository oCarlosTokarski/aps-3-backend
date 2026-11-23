from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schema.relatorio_schema import (
    EventosPorCategoria,
    OcupacaoEvento,
    ParticipacaoPorCurso
)
from service import relatorio_service


router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)


@router.get(
    "/eventos/ocupacao",
    response_model=list[OcupacaoEvento]
)
def ocupacao_eventos(db: Session = Depends(get_db)):
    return relatorio_service.relatorio_ocupacao(db)


@router.get(
    "/eventos/categorias",
    response_model=list[EventosPorCategoria]
)
def eventos_por_categoria(db: Session = Depends(get_db)):
    return relatorio_service.relatorio_categorias(db)


@router.get(
    "/participantes/cursos",
    response_model=list[ParticipacaoPorCurso]
)
def participacao_por_curso(db: Session = Depends(get_db)):
    return relatorio_service.relatorio_cursos(db)
