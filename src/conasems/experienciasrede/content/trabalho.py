# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.app.textfield import RichText
from zope import schema
from zope.interface import implementer
from plone.autoform import directives


# from conasems.experienciasrede import _


class ITrabalho(model.Schema):
    """Marker interface and Dexterity Python Schema for Trabalho"""

    title = schema.TextLine(
        title=u"Título",
        required=True,
    )

    codigo = schema.TextLine(
        title=u"Código",
        required=True,
    )

    autor = schema.TextLine(
        title=u"Autor",
        required=True,
    )

    funcao_autor = schema.TextLine(
        title=u"Função do Autor",
        required=False,
    )

    eixo_tematico = schema.TextLine(
        title=u"Eixo Temático",
        required=False,
    )

    coautor = schema.Text(
        title=u"Coautor",
        required=False,
    )

    cosems = schema.Choice(
        title=u"Cosems",
        required=False,
        values=[
            u"COSEMS Acre",
            u"COSEMS Alagoas",
            u"COSEMS Amapá",
            u"COSEMS Amazonas",
            u"COSEMS Bahia",
            u"COSEMS Ceará",
            u"COSEMS Distrito Federal",
            u"COSEMS Espírito Santo",
            u"COSEMS Goiás",
            u"COSEMS Maranhão",
            u"COSEMS Mato Grosso",
            u"COSEMS Mato Grosso do Sul",
            u"COSEMS Minas Gerais",
            u"COSEMS Pará",
            u"COSEMS Paraíba",
            u"COSEMS Paraná",
            u"COSEMS Pernambuco",
            u"COSEMS Piauí",
            u"COSEMS Rio de Janeiro",
            u"COSEMS Rio Grande do Norte",
            u"COSEMS Rio Grande do Sul",
            u"COSEMS Rondônia",
            u"COSEMS Roraima",
            u"COSEMS Santa Catarina",
            u"COSEMS São Paulo",
            u"COSEMS Sergipe",
            u"COSEMS Tocantins",
        ],
    )

    introducao = RichText(
        title=u"Introdução",
        required=False,
    )

    objetivos = RichText(
        title=u"Objetivos",
        required=False,
    )

    metodologia = RichText(
        title=u"Metodologia",
        required=False,
    )

    resultados_discussao = RichText(
        title=u"Resultados e Discussões",
        required=False,
    )

    consideracoes_finais = RichText(
        title=u"Considerações Finais",
        required=False,
    )

    referencias = RichText(
        title=u"Referências",
        required=False,
    )

    contato = schema.TextLine(
        title=u"Contato",
        required=False,
    )


@implementer(ITrabalho)
class Trabalho(Container):
    """Content-type class for ITrabalho"""
