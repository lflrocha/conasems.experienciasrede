# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api


UF_BY_COSEMS = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM',
    'Bahia': 'BA', 'Ceará': 'CE', 'Distrito Federal': 'DF',
    'Espírito Santo': 'ES', 'Goiás': 'GO', 'Maranhão': 'MA',
    'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG',
    'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE',
    'Piauí': 'PI', 'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS', 'Rondônia': 'RO', 'Roraima': 'RR',
    'Santa Catarina': 'SC', 'São Paulo': 'SP', 'Sergipe': 'SE',
    'Tocantins': 'TO',
}


class TrabalhosSelecionadosView(BrowserView):
    """View para listar trabalhos/experiências com busca e filtros no front."""

    portal_type = 'Trabalho'  # ajuste para o portal_type real do seu Dexterity

    @property
    def static_url(self):
        portal = api.portal.get()
        return portal.absolute_url() + '/++resource++experiencias-rede'

    def trabalhos(self):
        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())

        brains = catalog(
            portal_type=self.portal_type,
            path={'query': path, 'depth': 99},
            sort_on='codigo',
        )

        items = []
        for idx, brain in enumerate(brains, start=1):
            obj = brain.getObject()
            cosems = getattr(obj, 'cosems', '') or ''
            axis = getattr(obj, 'eixo_tematico', '') or ''
            author = getattr(obj, 'autor', '') or ''
            funcao = getattr(obj, 'funcao_autor', '') or ''
            codigo = getattr(obj, 'codigo', '') or ''
            uf = UF_BY_COSEMS.get(cosems, cosems)

            items.append({
                'id': 'ID-' + codigo,
                'title': obj.Title(),
                'author': author,
                'funcao': funcao,
                'cosems': cosems,
                'uf': uf,
                'axis': axis,
                'url': obj.absolute_url(),
            })

        return items

    def cosems_options(self):
        seen = []
        for item in self.trabalhos():
            uf = item['uf']
            if uf and uf not in seen:
                seen.append(uf)
        return sorted(seen)

    def axis_options(self):
        seen = []
        for item in self.trabalhos():
            axis = item['axis']
            if axis and axis not in seen:
                seen.append(axis)
        return sorted(seen)

try:
    from html import escape
except ImportError:  # pragma: no cover - Python 2 fallback
    from cgi import escape


class TrabalhoView(BrowserView):
    """View de detalhe para o tipo de conteúdo Trabalho/Experiência."""

    @property
    def static_url(self):
        portal = api.portal.get()
        return portal.absolute_url() + '/++resource++experiencias-rede'

    def _first_value(self, *names):
        for name in names:
            value = getattr(self.context, name, None)
            if value:
                return value
        return ''

    def _as_text(self, value):
        if value is None:
            return ''
        if hasattr(value, 'raw'):
            return value.raw or ''
        if hasattr(value, 'output'):
            return value.output or ''
        if isinstance(value, (list, tuple)):
            return ', '.join([self._as_text(item) for item in value if item])
        return value

    def _as_html(self, value):
        if value is None:
            return ''

        # RichTextValue do Plone já entrega HTML seguro em .output
        if hasattr(value, 'output') and value.output:
            return value.output

        text = self._as_text(value)
        if not text:
            return ''

        # Se já vier com HTML simples, mantém para preservar importações antigas.
        if '<p' in text or '<ul' in text or '<ol' in text or '<br' in text:
            return text

        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        return ''.join('<p>{}</p>'.format(escape(p)) for p in paragraphs)

    @property
    def autor(self):
        return self._as_text(self._first_value('autor', 'author'))

    @property
    def funcao_autor(self):
        return self._as_text(self._first_value('funcao_autor', 'funcaoAutor', 'funcao'))

    @property
    def coautor(self):
        return self._as_text(self._first_value('coautor', 'coautores'))

    @property
    def eixo_tematico(self):
        return self._as_text(self._first_value('eixo_tematico', 'eixoTematico', 'axis'))

    @property
    def cosems(self):
        return self._as_text(self._first_value('cosems', 'estado'))

    @property
    def uf(self):
        cosems = self.cosems
        return UF_BY_COSEMS.get(cosems, cosems)

    @property
    def identificador(self):
        return self._as_text(self._first_value('identificador', 'codigo', 'id_trabalho'))

    @property
    def introducao(self):
        return self._first_value('introducao', 'introduction')

    @property
    def introducao_html(self):
        return self._as_html(self.introducao)

    @property
    def objetivos(self):
        return self._first_value('objetivos', 'objetivo', 'objectives')

    @property
    def objetivos_html(self):
        return self._as_html(self.objetivos)

    @property
    def metodologia(self):
        return self._first_value('metodologia', 'methodology')

    @property
    def metodologia_html(self):
        return self._as_html(self.metodologia)

    @property
    def resultados(self):
        return self._first_value(
            'resultados_discussao',
            'resultados_e_discussoes',
            'resultadosDiscussao',
            'resultados',
        )

    @property
    def resultados_html(self):
        return self._as_html(self.resultados)

    @property
    def consideracoes_finais(self):
        return self._first_value('consideracoes_finais', 'consideracoesFinais', 'consideracoes')

    @property
    def consideracoes_finais_html(self):
        return self._as_html(self.consideracoes_finais)

    @property
    def referencias(self):
        return self._first_value('referencias', 'referências', 'bibliografia')

    @property
    def referencias_html(self):
        return self._as_html(self.referencias)

    @property
    def contato(self):
        return self._first_value('contato', 'email', 'e_mail')

    @property
    def contato_html(self):
        return self._as_html(self.contato)

    @property
    def back_url(self):
        parent = self.context.aq_parent
        if parent:
            return parent.absolute_url() + '/@@trabalhos-selecionados'
        portal = api.portal.get()
        return portal.absolute_url()
