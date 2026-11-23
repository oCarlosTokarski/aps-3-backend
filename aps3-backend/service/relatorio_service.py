from sqlalchemy import distinct, func

from model.evento import Evento
from model.inscricao import Inscricao
from model.participante import Participante


def relatorio_ocupacao(db):
    # outerjoin para incluir também eventos sem inscrições
    resultado = (
        db.query(
            Evento.id,
            Evento.titulo,
            Evento.capacidade,
            func.count(Inscricao.id)
        )
        .outerjoin(Inscricao, Inscricao.evento_id == Evento.id)
        .group_by(Evento.id)
        .all()
    )

    relatorio = []

    for evento_id, titulo, capacidade, total_inscritos in resultado:
        # Evita divisão por zero
        if capacidade > 0:
            percentual = round(total_inscritos / capacidade * 100, 2)
        else:
            percentual = 0.0

        relatorio.append({
            "evento_id": evento_id,
            "titulo": titulo,
            "capacidade": capacidade,
            "total_inscritos": total_inscritos,
            "vagas_disponiveis": capacidade - total_inscritos,
            "percentual_ocupacao": percentual
        })

    return relatorio


def relatorio_categorias(db):
    # Consulta 1: quantos eventos e quanta capacidade tem cada categoria
    eventos = (
        db.query(
            Evento.categoria,
            func.count(Evento.id),
            func.sum(Evento.capacidade)
        )
        .group_by(Evento.categoria)
        .all()
    )

    # Consulta 2: quantas inscrições tem cada categoria.
    # Fica separada porque, se juntasse com a consulta 1, a capacidade
    # do evento seria somada uma vez para cada inscrição.
    inscricoes = (
        db.query(Evento.categoria, func.count(Inscricao.id))
        .join(Inscricao, Inscricao.evento_id == Evento.id)
        .group_by(Evento.categoria)
        .all()
    )

    # Transforma em dicionário: {"Palestra": 10, "Workshop": 4, ...}
    inscricoes_por_categoria = dict(inscricoes)

    relatorio = []

    for categoria, total_eventos, capacidade_total in eventos:
        relatorio.append({
            "categoria": categoria,
            "total_eventos": total_eventos,
            "capacidade_total": capacidade_total,
            # Categoria sem nenhuma inscrição não aparece na consulta 2
            "total_inscricoes": inscricoes_por_categoria.get(categoria, 0)
        })

    return relatorio


def relatorio_cursos(db):
    # outerjoin: inclui participantes sem inscrição
    # distinct: não conta o mesmo participante duas vezes
    resultado = (
        db.query(
            Participante.curso,
            func.count(distinct(Participante.id)),
            func.count(Inscricao.id)
        )
        .outerjoin(Inscricao, Inscricao.participante_id == Participante.id)
        .group_by(Participante.curso)
        .all()
    )

    relatorio = []

    for curso, total_participantes, total_inscricoes in resultado:
        relatorio.append({
            "curso": curso,
            "total_participantes": total_participantes,
            "total_inscricoes": total_inscricoes
        })

    return relatorio
