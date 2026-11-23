from fastapi import FastAPI

from database import Base, engine
from controller.evento_controller import router as evento_router
from controller.participante_controller import router as participante_router
from controller.inscricao_controller import router as inscricao_router
from controller.relatorio_controller import router as relatorio_router

from model import evento, participante, inscricao

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API RESTful para gerenciamento de eventos e participantes.",
    version="3.0.0"
)

app.include_router(evento_router)
app.include_router(participante_router)
app.include_router(inscricao_router)
app.include_router(relatorio_router)
