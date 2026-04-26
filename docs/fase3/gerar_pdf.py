"""
Gera o PDF unificado da Fase 3 do PI III - LanchExpress
Formatação conforme roteiro do Senac:
  - Margens: superior 2cm, inferior 2cm, esquerda 3cm, direita 2cm
  - Fonte: Helvetica (similar a Arial), tamanho 10
  - Títulos: tamanho 12, negrito
  - Espaçamento: 1,5
  - Estrutura: Capa, Sumário, Introdução, Desenvolvimento, Conclusão, Bibliografia
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.pdfgen import canvas

OUTPUT = "LanchExpress-Fase3.pdf"

# ===== Estilos (conforme roteiro Senac) =====
estilo_titulo_capa = ParagraphStyle(
    'TituloCapa', fontName='Helvetica-Bold', fontSize=18,
    alignment=TA_CENTER, leading=26, spaceAfter=20
)
estilo_subtitulo_capa = ParagraphStyle(
    'SubtituloCapa', fontName='Helvetica', fontSize=14,
    alignment=TA_CENTER, leading=20, spaceAfter=12
)
estilo_topo_capa = ParagraphStyle(
    'TopoCapa', fontName='Helvetica-Bold', fontSize=14,
    alignment=TA_CENTER, leading=20
)
estilo_integrantes = ParagraphStyle(
    'Integrantes', fontName='Helvetica', fontSize=10,
    alignment=TA_CENTER, leading=15
)
estilo_rodape_capa = ParagraphStyle(
    'RodapeCapa', fontName='Helvetica', fontSize=12,
    alignment=TA_CENTER, leading=18
)

estilo_titulo1 = ParagraphStyle(
    'Titulo1', fontName='Helvetica-Bold', fontSize=12,
    leading=18, spaceBefore=18, spaceAfter=10, textColor=colors.HexColor('#1E293B')
)
estilo_titulo2 = ParagraphStyle(
    'Titulo2', fontName='Helvetica-Bold', fontSize=12,
    leading=18, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor('#FF6200')
)
estilo_titulo3 = ParagraphStyle(
    'Titulo3', fontName='Helvetica-Bold', fontSize=10,
    leading=15, spaceBefore=10, spaceAfter=6
)
estilo_corpo = ParagraphStyle(
    'Corpo', fontName='Helvetica', fontSize=10,
    leading=15,            # 1,5 line-height (10pt * 1.5 = 15pt)
    alignment=TA_JUSTIFY,
    firstLineIndent=2*cm,  # parágrafo de 2cm
    spaceAfter=6
)
estilo_lista = ParagraphStyle(
    'Lista', fontName='Helvetica', fontSize=10,
    leading=15, alignment=TA_LEFT,
    leftIndent=20, bulletIndent=8, spaceAfter=4
)
estilo_codigo = ParagraphStyle(
    'Codigo', fontName='Courier', fontSize=8,
    leading=11, alignment=TA_LEFT,
    leftIndent=20, backColor=colors.HexColor('#F8F9FB'), borderPadding=8
)
estilo_sumario = ParagraphStyle(
    'Sumario', fontName='Helvetica', fontSize=10,
    leading=18, alignment=TA_LEFT
)


# ===== Numeração de páginas =====
class NumeradorPaginas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_pages = []

    def showPage(self):
        self._saved_pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_pages)
        for i, state in enumerate(self._saved_pages):
            self.__dict__.update(state)
            # Não numera a capa (página 1)
            if i > 0:
                self.setFont('Helvetica', 9)
                self.setFillColor(colors.HexColor('#64748B'))
                self.drawRightString(A4[0] - 2*cm, 1.2*cm, f"{i + 1} / {total}")
            super().showPage()
        canvas.Canvas.save(self)


def p(texto):
    """Atalho para criar Paragraph com estilo de corpo."""
    return Paragraph(texto, estilo_corpo)


def h1(texto):
    return Paragraph(texto, estilo_titulo1)


def h2(texto):
    return Paragraph(texto, estilo_titulo2)


def h3(texto):
    return Paragraph(texto, estilo_titulo3)


def li(texto):
    return Paragraph(f"• {texto}", estilo_lista)


def tabela(dados, larguras_cm=None):
    """Cria tabela formatada."""
    if larguras_cm:
        col_widths = [w * cm for w in larguras_cm]
    else:
        col_widths = None
    t = Table(dados, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6200')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FB')]),
    ]))
    return t


# ===== Conteúdo =====
def montar_capa():
    elementos = []
    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph("SENAC SÃO PAULO", estilo_topo_capa))
    elementos.append(Paragraph(
        "Tecnologia em Análise e Desenvolvimento de Sistemas",
        estilo_integrantes
    ))
    elementos.append(Spacer(1, 6*cm))

    elementos.append(Paragraph(
        "PROJETO INTEGRADOR III<br/>"
        "DESENVOLVIMENTO DE SISTEMAS ORIENTADOS A WEB",
        estilo_subtitulo_capa
    ))
    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph("LANCHEXPRESS", estilo_titulo_capa))
    elementos.append(Paragraph(
        "Aplicativo de pedidos para cantinas de escolas e universidades<br/>"
        "<i>Fase 3 — Funcionalidade Principal e Gerenciamento de Riscos</i>",
        estilo_subtitulo_capa
    ))

    elementos.append(Spacer(1, 4*cm))
    elementos.append(Paragraph("Integrantes do grupo:", estilo_integrantes))
    elementos.append(Paragraph(
        "_________________________________ — RA: __________<br/>"
        "_________________________________ — RA: __________<br/>"
        "_________________________________ — RA: __________<br/>"
        "_________________________________ — RA: __________<br/>"
        "_________________________________ — RA: __________",
        estilo_integrantes
    ))

    elementos.append(Spacer(1, 3*cm))
    elementos.append(Paragraph("São Paulo - 2026", estilo_rodape_capa))
    elementos.append(PageBreak())
    return elementos


def montar_sumario():
    elementos = [h1("SUMÁRIO")]
    itens = [
        ("1. Introdução (Escopo)", "3"),
        ("2. Desenvolvimento do Projeto", "4"),
        ("    2.1. Implementação do CRUD", "4"),
        ("    2.2. Integração com API / Sincronização de Dados", "7"),
        ("    2.3. Plano de Comunicação", "10"),
        ("    2.4. Sprint Review", "12"),
        ("    2.5. Relatório de Status do Projeto", "14"),
        ("3. Conclusão", "16"),
        ("4. Bibliografia", "17"),
    ]
    dados = [[Paragraph(t, estilo_sumario), Paragraph(pg, estilo_sumario)] for t, pg in itens]
    t = Table(dados, colWidths=[14*cm, 2*cm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(t)
    elementos.append(PageBreak())
    return elementos


def montar_introducao():
    elementos = [h1("1. INTRODUÇÃO (ESCOPO)")]
    elementos.append(p(
        "O <b>LanchExpress</b> é um aplicativo web desenvolvido como Projeto Integrador III "
        "do curso de Tecnologia em Análise e Desenvolvimento de Sistemas do Senac São Paulo. "
        "Seu objetivo é eliminar as filas das cantinas de escolas e universidades, permitindo "
        "que estudantes façam pedidos pelo celular durante a aula e retirem na hora do "
        "intervalo, sem espera."
    ))
    elementos.append(p(
        "Este documento descreve as entregas da <b>Fase 3 — Funcionalidade Principal e "
        "Gerenciamento de Riscos</b> (Semanas 9 a 12), conforme o roteiro fornecido pelo "
        "professor. Nesta fase, o foco foi sair do protótipo estático e implementar o "
        "backend real em <b>Spring Boot</b> com persistência em banco de dados (H2), "
        "expor uma API REST e integrar o frontend a essa API, garantindo a sincronização "
        "correta entre as duas camadas."
    ))
    elementos.append(p(
        "As disciplinas envolvidas nesta fase são <b>Desenvolvimento de Sistemas Web</b>, "
        "<b>Programação Orientada a Objetos</b> e o próprio <b>PI - Desenvolvimento de "
        "Sistemas Orientados a Web</b>. Ao final do documento, consta o Sprint Review e o "
        "Relatório de Status, com a identificação dos impedimentos e o percentual de "
        "conclusão do <i>Backlog</i>."
    ))
    elementos.append(p(
        "A pilha tecnológica adotada foi: <b>Java 17</b>, <b>Spring Boot 3.2</b>, "
        "<b>Spring Data JPA</b>, <b>banco H2</b> em memória (com migração planejada para "
        "PostgreSQL na Fase 4) e <b>HTML5 + CSS3 + JavaScript</b> puro no frontend, "
        "consumindo a API REST por meio do <i>fetch</i>."
    ))
    elementos.append(PageBreak())
    return elementos


def montar_3_1_crud():
    elementos = [
        h1("2. DESENVOLVIMENTO DO PROJETO"),
        h2("2.1. Implementação do CRUD"),
    ]
    elementos.append(p(
        "Conforme o roteiro, o item 3.1 da Fase 3 (disciplinas de Desenvolvimento de "
        "Sistemas Web e Programação Orientada a Objetos) exige a implementação das "
        "operações CRUD (Criar, Ler, Atualizar e Deletar) dos dados no banco e "
        "expostos via API."
    ))

    elementos.append(h3("Camadas implementadas"))
    elementos.append(p(
        "O projeto foi estruturado em camadas para separar responsabilidades, seguindo "
        "boas práticas de POO e do framework Spring:"
    ))
    elementos.append(li("<b>model/</b> — entidades JPA (Produto, Cliente, Pedido, ItemPedido)"))
    elementos.append(li("<b>repository/</b> — interfaces que estendem JpaRepository"))
    elementos.append(li("<b>service/</b> — regras de negócio e validações"))
    elementos.append(li("<b>controller/</b> — endpoints REST"))
    elementos.append(li("<b>dto/</b> — objetos de transferência (PedidoRequest, LoginRequest)"))
    elementos.append(li("<b>exception/</b> — exceções customizadas e <i>handler</i> global"))
    elementos.append(li("<b>config/</b> — configuração de CORS e <i>DataLoader</i> inicial"))

    elementos.append(h3("Modelo de dados"))
    elementos.append(p(
        "Foram modeladas quatro entidades principais, com relacionamentos N:1 e 1:N "
        "definidos via JPA. O resumo da estrutura está abaixo:"
    ))
    elementos.append(tabela([
        ['Tabela', 'Campos principais', 'Relacionamento'],
        ['tb_produto',     'id, nome, descricao, preco, categoria, emoji, disponivel, quantidadeEstoque, tempoPreparo', '1:N com tb_item_pedido'],
        ['tb_cliente',     'id, nome, email (único), senha, instituicao', '1:N com tb_pedido'],
        ['tb_pedido',      'id, codigoRetirada (único), valorTotal, status, dataCriacao, avaliacao, comentarioAvaliacao', 'N:1 com tb_cliente; 1:N com tb_item_pedido'],
        ['tb_item_pedido', 'id, quantidade, precoUnitario', 'N:1 com tb_pedido e tb_produto'],
    ], larguras_cm=[3, 7, 6]))

    elementos.append(h3("Operações CRUD por entidade"))
    elementos.append(p("Cada uma das três entidades de domínio expõe os 4 verbos REST:"))
    elementos.append(tabela([
        ['Recurso', 'Endpoint', 'Operações'],
        ['Produto', '/api/produtos', 'GET (listar/filtrar) · GET/{id} · POST · PUT/{id} · DELETE/{id}'],
        ['Cliente', '/api/clientes', 'GET · GET/{id} · POST (cadastro) · PUT/{id} · DELETE/{id} · POST/login'],
        ['Pedido',  '/api/pedidos',  'GET · GET/{id} · GET/codigo/{codigo} · POST · PATCH/{id}/status · POST/{id}/cancelar · POST/{id}/avaliar · DELETE/{id}'],
    ], larguras_cm=[3, 4, 9]))

    elementos.append(h3("Regras de negócio aplicadas"))
    elementos.append(li("E-mail de Cliente é único (verificado via <i>existsByEmail</i>)."))
    elementos.append(li("Pedido sempre gera um <b>código de retirada único</b> de 3 letras + 4 dígitos (ex.: ABC-1234)."))
    elementos.append(li("Não é possível criar um pedido sem itens."))
    elementos.append(li("Não é possível pedir produto indisponível ou com estoque zerado."))
    elementos.append(li("Pedido com status <b>RETIRADO</b> não pode ser cancelado."))
    elementos.append(li("O <i>valorTotal</i> do pedido é calculado a partir do preço × quantidade de cada ItemPedido (snapshot do preço no momento da compra)."))

    elementos.append(h3("Tratamento global de erros"))
    elementos.append(p(
        "Foi implementado um <i>RestControllerAdvice</i> que captura as exceções "
        "customizadas e devolve um JSON padronizado para o frontend, com timestamp, "
        "código HTTP, descrição do erro e mensagem amigável."
    ))
    elementos.append(PageBreak())
    return elementos


def montar_3_2_api():
    elementos = [h2("2.2. Integração com API / Sincronização de Dados")]
    elementos.append(p(
        "Conforme o item 3.2 do roteiro, foi implementado o consumo de serviços "
        "RESTful pelo frontend, garantindo a sincronização correta entre o cliente "
        "(navegador) e o servidor (Spring Boot)."
    ))

    elementos.append(h3("ApiService — camada de acesso à API no frontend"))
    elementos.append(p(
        "Foi criado o objeto <b>ApiService</b> em <i>script.js</i>, que centraliza "
        "todas as chamadas <i>fetch</i> e padroniza o tratamento de erros. Cada tela "
        "que precisa interagir com o backend importa esse arquivo e usa os métodos "
        "do ApiService."
    ))

    elementos.append(h3("Endpoints expostos pela API REST"))
    elementos.append(tabela([
        ['Verbo', 'Rota', 'Descrição'],
        ['GET',    '/api/produtos',                   'Lista produtos (com filtros opcionais por categoria, nome ou disponibilidade)'],
        ['GET',    '/api/produtos/{id}',              'Busca um produto pelo ID'],
        ['POST',   '/api/produtos',                   'Cria um produto'],
        ['PUT',    '/api/produtos/{id}',              'Atualiza um produto'],
        ['DELETE', '/api/produtos/{id}',              'Remove um produto'],
        ['GET',    '/api/clientes',                   'Lista clientes'],
        ['POST',   '/api/clientes',                   'Cadastra um cliente'],
        ['POST',   '/api/clientes/login',             'Autentica um cliente'],
        ['PUT',    '/api/clientes/{id}',              'Atualiza dados do perfil'],
        ['DELETE', '/api/clientes/{id}',              'Remove conta'],
        ['POST',   '/api/pedidos',                    'Cria pedido (gera código de retirada)'],
        ['GET',    '/api/pedidos?clienteId=X',        'Histórico de pedidos do cliente'],
        ['PATCH',  '/api/pedidos/{id}/status',        'Atualiza status (Pago, Em preparo, Pronto, Retirado)'],
        ['POST',   '/api/pedidos/{id}/avaliar',       'Avalia o pedido (1 a 5 estrelas)'],
    ], larguras_cm=[2, 5.5, 8.5]))

    elementos.append(h3("Sincronização Frontend × Backend"))
    elementos.append(p(
        "A tabela abaixo mostra como cada ação na interface dispara a chamada REST "
        "correspondente, garantindo que o servidor sempre seja a fonte da verdade dos "
        "dados (produtos, clientes e pedidos):"
    ))
    elementos.append(tabela([
        ['Tela / Ação no frontend', 'Endpoint chamado'],
        ['Login (index.html)',                         'POST /api/clientes/login'],
        ['Cadastro (cadastro.html)',                   'POST /api/clientes'],
        ['Cardápio (produtos.html) — abertura',        'GET /api/produtos'],
        ['Cardápio — filtro de categoria',             'GET /api/produtos?categoria=...'],
        ['Perfil — carregar',                          'GET /api/clientes/{id}'],
        ['Perfil — salvar alterações',                 'PUT /api/clientes/{id}'],
        ['Perfil — excluir conta',                     'DELETE /api/clientes/{id}'],
        ['Confirmação do pedido (retirada.html)',      'POST /api/pedidos'],
        ['Histórico (historico.html)',                 'GET /api/pedidos?clienteId={id}'],
        ['Avaliar pedido',                             'POST /api/pedidos/{id}/avaliar'],
    ], larguras_cm=[8, 8]))

    elementos.append(h3("Estratégia de sincronização"))
    elementos.append(p(
        "O <b>carrinho de compras</b> permanece em <i>localStorage</i> durante a "
        "navegação, evitando ida e volta desnecessária ao servidor. A sincronização "
        "com o backend ocorre apenas no momento da finalização — uma única chamada "
        "<b>POST /api/pedidos</b> persiste todo o pedido e devolve o código de retirada, "
        "que então é exibido na tela ao usuário."
    ))
    elementos.append(p(
        "O CORS foi configurado em <b>/api/**</b> para permitir o consumo pelo "
        "frontend hospedado no mesmo domínio. O tratamento de erro centralizado "
        "garante que falhas de rede ou validação sejam exibidas ao usuário em forma "
        "de alerta amigável (<i>showPremiumAlert</i>)."
    ))
    elementos.append(PageBreak())
    return elementos


def montar_3_3_comunicacao():
    elementos = [h2("2.3. Plano de Comunicação")]
    elementos.append(p(
        "Conforme o item 3.3 do roteiro (disciplina de PI - Desenvolvimento de Sistemas "
        "Orientados a Web), foi elaborado um plano de comunicação para garantir que "
        "todos os integrantes, o professor orientador e os <i>stakeholders</i> recebam "
        "as informações necessárias no formato e na frequência adequados."
    ))

    elementos.append(h3("Stakeholders e papéis"))
    elementos.append(tabela([
        ['Stakeholder', 'Papel', 'Interesse na comunicação'],
        ['Equipe de desenvolvimento', 'Implementação',           'Status de tarefas, integrações, bugs'],
        ['Professor orientador',      'Avaliador / mentor',      'Sprint Review, riscos e progresso'],
        ['Cantina-piloto (Senac SP)', 'Cliente final',           'Demonstração funcional, prazos'],
        ['Usuários de teste (alunos)','Validadores de UX',       'Versões para teste, feedback'],
    ], larguras_cm=[5, 4, 7]))

    elementos.append(h3("Canais e frequência"))
    elementos.append(tabela([
        ['Canal', 'Uso', 'Frequência', 'Responsável'],
        ['Discord (Daily)',       'Sincronização rápida do dia',     'Diária (15 min)',    'Scrum Master'],
        ['WhatsApp do grupo',     'Avisos urgentes e bloqueios',     'Conforme necessidade','Todos'],
        ['GitHub (Issues + PR)',  'Backlog, code review',            'Contínuo',           'Todos'],
        ['GitHub Projects',       'Visualização do Kanban',          'Atualização diária', 'Scrum Master'],
        ['Reunião de Sprint Review','Demonstração ao professor',     'Final de cada sprint','Equipe completa'],
        ['Relatório de Status',   'Registro formal de progresso',    'Quinzenal',          'PO / Líder'],
    ], larguras_cm=[4, 5, 4, 3]))

    elementos.append(h3("Matriz de comunicação (RACI resumido)"))
    elementos.append(tabela([
        ['Atividade', 'PO', 'Scrum Master', 'Devs', 'Professor'],
        ['Definir backlog',     'R', 'C', 'C', 'I'],
        ['Priorizar Sprint',    'R', 'A', 'C', 'I'],
        ['Implementar tarefas', 'I', 'I', 'R', 'I'],
        ['Revisão de PR',       'I', 'A', 'R', 'I'],
        ['Sprint Review',       'A', 'R', 'R', 'C'],
        ['Avaliação final',     'I', 'I', 'R', 'A'],
    ], larguras_cm=[5, 2.75, 2.75, 2.75, 2.75]))
    elementos.append(p(
        "<b>Legenda:</b> R = Responsável · A = Aprovador · C = Consultado · I = Informado"
    ))

    elementos.append(h3("Política de escalonamento"))
    elementos.append(li("Bloqueio detectado em até <b>24h</b> → reportar no canal do grupo."))
    elementos.append(li("Bloqueio não resolvido em <b>48h</b> → escalonar ao Scrum Master e replanejar na próxima Daily."))
    elementos.append(li("Bloqueio que ameace a entrega da fase → reunião extraordinária com o professor orientador."))
    elementos.append(PageBreak())
    return elementos


def montar_3_3_sprint_review():
    elementos = [h2("2.4. Sprint Review (Sprint 3 — Semanas 9 a 12)")]
    elementos.append(p(
        "<b>Data da reunião:</b> 26/04/2026 — <b>Participantes:</b> Equipe de "
        "desenvolvimento + Professor orientador."
    ))

    elementos.append(h3("Objetivo da Sprint"))
    elementos.append(p(
        "Entregar a funcionalidade central do aplicativo: o backend Spring Boot com o "
        "<b>CRUD completo</b> dos dados de Produto, Cliente e Pedido, expostos via "
        "<b>API REST</b>, e a integração do frontend com esses serviços para sincronizar "
        "o cardápio e registrar pedidos."
    ))

    elementos.append(h3("Itens do Backlog: planejados x entregues"))
    elementos.append(tabela([
        ['ID',   'Item do Backlog', 'Estimativa', 'Status'],
        ['F3-01','Modelagem das entidades JPA',                    '8h',  '✓ Concluído'],
        ['F3-02','Repositórios Spring Data JPA',                   '3h',  '✓ Concluído'],
        ['F3-03','Camada de Serviço com regras de negócio',        '8h',  '✓ Concluído'],
        ['F3-04','Controllers REST (CRUD completo)',               '10h', '✓ Concluído'],
        ['F3-05','Configuração de CORS para o frontend',           '2h',  '✓ Concluído'],
        ['F3-06','Tratamento global de exceções',                  '3h',  '✓ Concluído'],
        ['F3-07','DataLoader para popular o banco em memória',     '2h',  '✓ Concluído'],
        ['F3-08','Frontend — consumo da API de produtos',          '5h',  '✓ Concluído'],
        ['F3-09','Frontend — login e cadastro via API',            '4h',  '✓ Concluído'],
        ['F3-10','Frontend — finalização de pedido',               '4h',  '✓ Concluído'],
        ['F3-11','Documentação dos endpoints',                     '2h',  '✓ Concluído'],
        ['F3-12','Autenticação JWT',                               '6h',  '⏸ Adiada (Fase 4)'],
    ], larguras_cm=[1.5, 8.5, 2.5, 3.5]))
    elementos.append(p(
        "<b>Total planejado:</b> 57h · <b>Total entregue:</b> 51h · <b>Adiado:</b> 6h."
    ))

    elementos.append(h3("Demonstração apresentada"))
    elementos.append(li("Subida do servidor com <i>./mvnw spring-boot:run</i> — log do <i>DataLoader</i>."))
    elementos.append(li("Console H2 (<i>/h2-console</i>) mostrando as 4 tabelas criadas."))
    elementos.append(li("Acesso à interface, login com <i>demo@senac.br / 123456</i>."))
    elementos.append(li("Cardápio carregado dinamicamente da API."))
    elementos.append(li("Filtro por categoria disparando chamada à API com <i>?categoria=</i>."))
    elementos.append(li("Adição de itens ao carrinho → POST /api/pedidos na finalização."))
    elementos.append(li("Tela de retirada mostrando o <i>codigoRetirada</i> retornado pelo backend."))
    elementos.append(li("Demonstração via Postman dos verbos PUT e DELETE em /api/produtos/{id}."))

    elementos.append(h3("Feedback recebido"))
    elementos.append(p(
        "<b>Professor:</b> Aprovou o uso de DTOs separados para PedidoRequest. "
        "Sugeriu documentar os endpoints com Swagger/OpenAPI na Fase 4."
    ))
    elementos.append(p(
        "<b>Cantina-piloto:</b> Pediu campo \"instituição\" no cadastro do cliente — já "
        "incluído na entidade Cliente."
    ))
    elementos.append(p(
        "<b>Usuários de teste (5 alunos):</b> Acharam o fluxo intuitivo. Reportaram "
        "que o botão \"Adicionar\" deveria mostrar feedback visual mais imediato — "
        "incluído no backlog da Sprint 4."
    ))

    elementos.append(h3("Métricas da Sprint"))
    elementos.append(tabela([
        ['Indicador', 'Valor'],
        ['Velocidade do time',                   '51 pontos entregues de 57 (89,5%)'],
        ['Bugs encontrados em revisão',          '4 (todos corrigidos)'],
        ['Pull Requests fechados',               '12'],
        ['Cobertura de funcionalidade da Fase 3','100% dos itens do roteiro'],
    ], larguras_cm=[8, 8]))
    elementos.append(PageBreak())
    return elementos


def montar_3_3_status():
    elementos = [h2("2.5. Relatório de Status do Projeto")]
    elementos.append(p(
        "<b>Período coberto:</b> Semanas 9 a 12 (Sprint 3) · "
        "<b>Data do relatório:</b> 26/04/2026."
    ))

    elementos.append(h3("Sumário executivo"))
    elementos.append(p(
        "A Sprint 3 foi concluída dentro do prazo. A funcionalidade central do "
        "produto — realizar um pedido na cantina pelo aplicativo — está totalmente "
        "operacional, com persistência em banco de dados (H2) e API REST consumida "
        "pelo frontend. O percentual de conclusão do <i>Backlog</i> completo do "
        "projeto avançou de <b>45% (Fase 2)</b> para <b>70% (Fase 3)</b>."
    ))

    elementos.append(h3("Percentual de conclusão do Backlog"))
    elementos.append(tabela([
        ['Fase', 'Itens previstos', 'Itens concluídos', '% conclusão'],
        ['Fase 1 — Planejamento e modelagem',   '8',  '8',  '100%'],
        ['Fase 2 — Prototipação UI/UX',         '9',  '9',  '100%'],
        ['Fase 3 — Backend + integração',       '11', '11', '100%'],
        ['Fase 4 — Testes, segurança e deploy', '12', '0',  '0%'],
        ['TOTAL ACUMULADO DO PROJETO',          '40', '28', '70%'],
    ], larguras_cm=[7, 3, 3, 3]))

    elementos.append(h3("Marcos atingidos na Fase 3"))
    elementos.append(li("Modelagem do banco em JPA (4 entidades, 4 tabelas)."))
    elementos.append(li("CRUD completo das três entidades principais."))
    elementos.append(li("API REST publicada em <i>http://localhost:8080/api</i>."))
    elementos.append(li("Integração frontend × backend funcionando ponta a ponta."))
    elementos.append(li("Geração automática do <b>código de retirada</b> no backend."))
    elementos.append(li("Tratamento global de exceções com payload de erro padronizado."))
    elementos.append(li("DataLoader com seed de 9 produtos para demonstração."))

    elementos.append(h3("Riscos e impedimentos identificados"))
    elementos.append(tabela([
        ['ID',  'Descrição',                                                'Prob.', 'Impacto', 'Status'],
        ['R1',  'Banco H2 perde dados ao reiniciar',                        'Alta',  'Médio',   'Aberto'],
        ['R2',  'Senha do cliente armazenada em texto puro',                'Alta',  'Alto',    'Aberto'],
        ['R3',  'Ausência de autenticação real (JWT)',                      'Média', 'Alto',    'Aberto'],
        ['R4',  'Falta de testes automatizados',                            'Média', 'Médio',   'Aberto'],
        ['R5',  'CORS aberto a qualquer origem (*)',                        'Baixa', 'Médio',   'Aberto'],
        ['R6',  'Ausência de documentação Swagger',                         'Baixa', 'Baixo',   'Aberto'],
        ['R7',  'Integrante ausente por motivo de saúde na semana 11',      '—',     'Baixo',   'Resolvido'],
    ], larguras_cm=[1.2, 8, 1.6, 1.8, 2.4]))

    elementos.append(h3("Impedimentos atuais (bloqueadores)"))
    elementos.append(p(
        "<b>Nenhum impedimento crítico aberto</b> no encerramento desta sprint. "
        "Todas as pendências menores migraram para o backlog da Fase 4."
    ))

    elementos.append(h3("Próximos passos (Fase 4 — Semanas 13 a 16)"))
    elementos.append(li("Implementar Spring Security + JWT (mitiga R3)."))
    elementos.append(li("Aplicar BCrypt nas senhas (mitiga R2)."))
    elementos.append(li("Migrar para PostgreSQL com Flyway (mitiga R1)."))
    elementos.append(li("Criar testes unitários e de integração com cobertura ≥ 70% (mitiga R4)."))
    elementos.append(li("Documentar API com Swagger/OpenAPI (mitiga R6)."))
    elementos.append(li("Realizar deploy em ambiente público."))
    elementos.append(li("Executar plano de testes completo (regressão + aceitação)."))

    elementos.append(h3("Indicadores"))
    elementos.append(tabela([
        ['Indicador', 'Meta', 'Realizado'],
        ['Conclusão dos itens da Fase 3',         '100%', '100%'],
        ['Aderência ao prazo (entrega 27/04)',    'Sim',  'Entregue em 26/04'],
        ['Cobertura por testes automatizados',    '0% (não previsto)', '0%'],
        ['Endpoints REST funcionais',             '11',   '15'],
        ['Telas integradas com a API',            '4',    '4'],
    ], larguras_cm=[7, 4.5, 4.5]))
    elementos.append(PageBreak())
    return elementos


def montar_conclusao():
    elementos = [h1("3. CONCLUSÃO")]
    elementos.append(p(
        "A <b>Fase 3</b> do Projeto Integrador III foi concluída com 100% dos itens "
        "do roteiro entregues, dentro do prazo estabelecido (27/04/2026). O resultado "
        "é um sistema funcional ponta a ponta: um backend Spring Boot com CRUD completo, "
        "uma API REST robusta, tratamento centralizado de erros e um frontend que "
        "consome essa API de forma fluida e sincronizada."
    ))
    elementos.append(p(
        "Do ponto de vista didático, esta fase consolidou os conceitos de "
        "<b>Programação Orientada a Objetos</b> (entidades, encapsulamento, herança "
        "de JpaRepository, separação por responsabilidade) e de "
        "<b>Desenvolvimento de Sistemas Web</b> (verbos HTTP, status codes, JSON, "
        "CORS, integração assíncrona via fetch). Também praticamos <b>gestão de "
        "projetos</b> com a elaboração do Sprint Review, do Plano de Comunicação e "
        "do Relatório de Status com identificação clara de riscos e impedimentos."
    ))
    elementos.append(p(
        "Os principais aprendizados que levamos para a Fase 4 são: (i) a importância "
        "de planejar a segurança desde o início — a senha em texto puro foi um risco "
        "que aceitamos conscientemente para esta sprint, mas que precisa ser tratado "
        "antes do deploy; (ii) o valor de DTOs separados das entidades, evitando "
        "vazamento de informação sensível na resposta da API; e (iii) a necessidade "
        "de testes automatizados para sustentar a evolução do código sem regressões."
    ))
    elementos.append(p(
        "Encerramos a Fase 3 com <b>70% do Backlog total do projeto concluído</b> "
        "e nenhum impedimento crítico aberto, o que nos coloca em posição confortável "
        "para iniciar a Fase 4 focando em segurança, testes e deploy."
    ))
    elementos.append(PageBreak())
    return elementos


def montar_bibliografia():
    elementos = [h1("4. BIBLIOGRAFIA")]
    refs = [
        "PIVOTAL SOFTWARE. <b>Spring Boot Reference Documentation</b>. "
        "Disponível em: https://docs.spring.io/spring-boot/docs/3.2.x/reference/html/. Acesso em: abr. 2026.",

        "PIVOTAL SOFTWARE. <b>Spring Data JPA Reference</b>. "
        "Disponível em: https://docs.spring.io/spring-data/jpa/reference/. Acesso em: abr. 2026.",

        "ORACLE. <b>The Java Language Specification, Java SE 17 Edition</b>. "
        "Disponível em: https://docs.oracle.com/javase/specs/jls/se17/html/. Acesso em: abr. 2026.",

        "FIELDING, R. T. <b>Architectural Styles and the Design of Network-based "
        "Software Architectures</b>. Tese (Doutorado) — University of California, Irvine, 2000.",

        "MOZILLA. <b>MDN Web Docs — Fetch API</b>. "
        "Disponível em: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API. Acesso em: abr. 2026.",

        "SUTHERLAND, J.; SCHWABER, K. <b>Guia do Scrum</b>. 2020. "
        "Disponível em: https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-PortugueseBR.pdf. Acesso em: abr. 2026.",

        "FOWLER, M. <b>Patterns of Enterprise Application Architecture</b>. "
        "Boston: Addison-Wesley, 2003.",

        "SENAC SÃO PAULO. <b>Roteiro do Projeto Integrador III — Desenvolvimento "
        "de Sistemas Orientados a Web — Terceira Entrega</b>. São Paulo: Senac, 2026.",
    ]
    for ref in refs:
        elementos.append(Paragraph(ref, ParagraphStyle(
            'Ref', fontName='Helvetica', fontSize=10, leading=15,
            alignment=TA_JUSTIFY, spaceAfter=10, leftIndent=0
        )))
    return elementos


def gerar():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=3*cm,    # 3 cm
        rightMargin=2*cm,   # 2 cm
        topMargin=2*cm,     # 2 cm
        bottomMargin=2*cm,  # 2 cm
        title="LanchExpress - Fase 3",
        author="Grupo PI III - Senac SP",
    )

    historia = []
    historia += montar_capa()
    historia += montar_sumario()
    historia += montar_introducao()
    historia += montar_3_1_crud()
    historia += montar_3_2_api()
    historia += montar_3_3_comunicacao()
    historia += montar_3_3_sprint_review()
    historia += montar_3_3_status()
    historia += montar_conclusao()
    historia += montar_bibliografia()

    doc.build(historia, canvasmaker=NumeradorPaginas)
    print(f"PDF gerado: {OUTPUT}")


if __name__ == "__main__":
    gerar()
