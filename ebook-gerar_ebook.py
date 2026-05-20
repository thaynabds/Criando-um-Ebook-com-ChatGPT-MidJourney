"""
Gerador do eBook: IA na Prática — Do Zero ao Primeiro Projeto com ChatGPT
Autora: Thayná Batista da Silva
Desafio DIO — Bootcamp Bradesco GenAI & Dados
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
import os

# ── PALETA DE CORES ──────────────────────────────────────────────────────────
C_BG_DARK   = colors.HexColor("#0F0F1A")
C_PURPLE    = colors.HexColor("#7C3AED")
C_PURPLE_L  = colors.HexColor("#A78BFA")
C_CYAN      = colors.HexColor("#06B6D4")
C_CYAN_L    = colors.HexColor("#67E8F9")
C_WHITE     = colors.HexColor("#F8FAFC")
C_MUTED     = colors.HexColor("#94A3B8")
C_CARD      = colors.HexColor("#1E1B4B")
C_GOLD      = colors.HexColor("#F59E0B")
C_GREEN     = colors.HexColor("#10B981")
C_DARK_BG2  = colors.HexColor("#13111F")
C_BORDER    = colors.HexColor("#312E81")

W, H = A4

# ── ESTILOS ───────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "cover_title": ParagraphStyle("cover_title",
            fontName="Helvetica-Bold", fontSize=38,
            textColor=C_WHITE, alignment=TA_CENTER,
            leading=46, spaceAfter=8),

        "cover_subtitle": ParagraphStyle("cover_subtitle",
            fontName="Helvetica", fontSize=17,
            textColor=C_CYAN_L, alignment=TA_CENTER,
            leading=24, spaceAfter=6),

        "cover_author": ParagraphStyle("cover_author",
            fontName="Helvetica-Bold", fontSize=12,
            textColor=C_PURPLE_L, alignment=TA_CENTER,
            leading=18),

        "cover_meta": ParagraphStyle("cover_meta",
            fontName="Helvetica", fontSize=10,
            textColor=C_MUTED, alignment=TA_CENTER, leading=16),

        "chapter_num": ParagraphStyle("chapter_num",
            fontName="Helvetica-Bold", fontSize=13,
            textColor=C_CYAN, alignment=TA_LEFT,
            leading=18, spaceAfter=4),

        "chapter_title": ParagraphStyle("chapter_title",
            fontName="Helvetica-Bold", fontSize=26,
            textColor=C_WHITE, alignment=TA_LEFT,
            leading=32, spaceAfter=6),

        "section_title": ParagraphStyle("section_title",
            fontName="Helvetica-Bold", fontSize=14,
            textColor=C_PURPLE_L, alignment=TA_LEFT,
            leading=20, spaceBefore=14, spaceAfter=5),

        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=11,
            textColor=C_WHITE, alignment=TA_JUSTIFY,
            leading=19, spaceAfter=10),

        "body_muted": ParagraphStyle("body_muted",
            fontName="Helvetica", fontSize=10,
            textColor=C_MUTED, alignment=TA_JUSTIFY,
            leading=17, spaceAfter=8),

        "tip_title": ParagraphStyle("tip_title",
            fontName="Helvetica-Bold", fontSize=11,
            textColor=C_GOLD, alignment=TA_LEFT, leading=16),

        "tip_body": ParagraphStyle("tip_body",
            fontName="Helvetica", fontSize=10,
            textColor=C_WHITE, alignment=TA_JUSTIFY, leading=16),

        "code": ParagraphStyle("code",
            fontName="Courier", fontSize=9,
            textColor=C_CYAN_L, alignment=TA_LEFT,
            leading=14, spaceAfter=4),

        "toc_chapter": ParagraphStyle("toc_chapter",
            fontName="Helvetica-Bold", fontSize=12,
            textColor=C_WHITE, alignment=TA_LEFT, leading=20),

        "toc_page": ParagraphStyle("toc_page",
            fontName="Helvetica", fontSize=11,
            textColor=C_CYAN, alignment=TA_LEFT, leading=20),

        "quote": ParagraphStyle("quote",
            fontName="Helvetica-Oblique", fontSize=13,
            textColor=C_CYAN_L, alignment=TA_CENTER,
            leading=20, spaceAfter=8, spaceBefore=8),

        "bullet": ParagraphStyle("bullet",
            fontName="Helvetica", fontSize=11,
            textColor=C_WHITE, alignment=TA_LEFT,
            leading=19, spaceAfter=5, leftIndent=16),

        "page_title": ParagraphStyle("page_title",
            fontName="Helvetica-Bold", fontSize=20,
            textColor=C_WHITE, alignment=TA_CENTER,
            leading=28, spaceAfter=16),

        "highlight": ParagraphStyle("highlight",
            fontName="Helvetica-Bold", fontSize=11,
            textColor=C_GREEN, alignment=TA_LEFT, leading=18),
    }


# ── FLOWABLES CUSTOMIZADOS ────────────────────────────────────────────────────
class DarkRect(Flowable):
    """Retângulo de fundo escuro para toda a página."""
    def __init__(self, w, h, color):
        super().__init__()
        self.w, self.h, self.color = w, h, color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.w, self.h, fill=1, stroke=0)


class GlowLine(Flowable):
    """Linha decorativa com gradiente."""
    def __init__(self, width=None, color=None):
        super().__init__()
        self._width = width or (W - 40*mm)
        self._color = color or C_PURPLE
        self.height = 3

    def wrap(self, *args):
        return self._width, self.height

    def draw(self):
        self.canv.setStrokeColor(self._color)
        self.canv.setLineWidth(2)
        self.canv.line(0, 0, self._width, 0)


class TipBox(Flowable):
    """Caixa de dica com fundo colorido."""
    def __init__(self, icon, title, text, width, styles):
        super().__init__()
        self._icon = icon
        self._title = title
        self._text = text
        self._width = width
        self._styles = styles

    def wrap(self, availWidth, availHeight):
        self._w = min(self._width, availWidth)
        return self._w, 72

    def draw(self):
        c = self.canv
        w, h = self._w, 68
        # Card bg
        c.setFillColor(C_CARD)
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)
        # Left accent bar
        c.setFillColor(C_GOLD)
        c.rect(0, 0, 4, h, fill=1, stroke=0)
        # Icon + title
        c.setFillColor(C_GOLD)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(12, h - 20, f"{self._icon}  {self._title}")
        # Body text
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica", 9)
        lines = self._wrap_text(self._text, w - 20, 9)
        y = h - 36
        for line in lines[:3]:
            c.drawString(12, y, line)
            y -= 13

    def _wrap_text(self, text, max_w, font_size):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = cur + (" " if cur else "") + w
            if len(test) * font_size * 0.55 < max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines


class ChapterHeader(Flowable):
    """Cabeçalho de capítulo com design escuro."""
    def __init__(self, num, title, subtitle, width):
        super().__init__()
        self._num = num
        self._title = title
        self._sub = subtitle
        self._width = width
        self.height = 110

    def wrap(self, *args):
        return self._width, self.height

    def draw(self):
        c = self.canv
        w, h = self._width, self.height
        # Background
        c.setFillColor(C_DARK_BG2)
        c.roundRect(0, 0, w, h, 8, fill=1, stroke=0)
        # Accent top bar
        c.setFillColor(C_PURPLE)
        c.rect(0, h - 4, w, 4, fill=1, stroke=0)
        # Chapter number badge
        c.setFillColor(C_PURPLE)
        c.roundRect(16, h - 44, 80, 26, 13, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(56, h - 35, self._num)
        # Title
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(16, h - 70, self._title)
        # Subtitle
        c.setFillColor(C_CYAN)
        c.setFont("Helvetica", 10)
        c.drawString(16, h - 88, self._sub)
        # Decorative dot row
        c.setFillColor(C_PURPLE)
        for i in range(8):
            c.circle(w - 20 - i*14, 20, 3, fill=1, stroke=0)


# ── PAGE TEMPLATE ─────────────────────────────────────────────────────────────
def make_page_template(is_cover=False):
    def on_page(canv, doc):
        canv.saveState()
        # Full dark background
        canv.setFillColor(C_BG_DARK)
        canv.rect(0, 0, W, H, fill=1, stroke=0)

        if is_cover:
            # Decorative circles
            canv.setFillColor(colors.HexColor("#1E1B4B"))
            canv.circle(W - 60, H - 60, 120, fill=1, stroke=0)
            canv.setFillColor(colors.HexColor("#1a1040"))
            canv.circle(60, 80, 90, fill=1, stroke=0)
            canv.setFillColor(C_PURPLE)
            canv.setFillAlpha(0.08)
            canv.circle(W/2, H/2, 220, fill=1, stroke=0)
            canv.setFillAlpha(1)
        else:
            # Header line
            canv.setStrokeColor(C_BORDER)
            canv.setLineWidth(0.5)
            canv.line(20*mm, H - 14*mm, W - 20*mm, H - 14*mm)
            # Header text
            canv.setFillColor(C_MUTED)
            canv.setFont("Helvetica", 8)
            canv.drawString(20*mm, H - 12*mm, "IA na Prática")
            canv.drawRightString(W - 20*mm, H - 12*mm, "Thayná Batista da Silva")
            # Footer line
            canv.line(20*mm, 12*mm, W - 20*mm, 12*mm)
            # Page number
            canv.setFillColor(C_MUTED)
            canv.setFont("Helvetica", 8)
            canv.drawCentredString(W/2, 8*mm, str(doc.page))
            # Subtle corner accent
            canv.setStrokeColor(C_PURPLE)
            canv.setLineWidth(1.5)
            canv.line(20*mm, H - 14*mm, 20*mm + 30, H - 14*mm)

        canv.restoreState()

    return on_page


# ── CONTEÚDO DOS CAPÍTULOS ────────────────────────────────────────────────────
CHAPTERS = [
    {
        "num": "CAPÍTULO 01",
        "title": "O Que é Inteligência Artificial",
        "sub": "Desmistificando a tecnologia que está transformando o mundo",
        "sections": [
            {
                "title": "🤖 IA: Muito Além da Ficção Científica",
                "body": [
                    "Quando ouvimos Inteligência Artificial, é comum imaginarmos robôs futuristas ou computadores tomando o controle do mundo. A realidade, porém, é bem mais fascinante — e muito mais próxima do nosso cotidiano do que imaginamos.",
                    "A Inteligência Artificial é um campo da ciência da computação dedicado a criar sistemas capazes de realizar tarefas que normalmente exigiriam inteligência humana: reconhecer padrões, tomar decisões, aprender com experiências e até criar conteúdo original.",
                    "Você já usou IA hoje? Se você fez uma pesquisa no Google, recebeu uma recomendação no Spotify, usou o filtro de spam do e-mail ou conversou com um chatbot de atendimento, a resposta é sim — provavelmente várias vezes.",
                ],
                "tip": ("💡 Dica Rápida", "Mapeie sua rotina e identifique onde a IA já está presente. Você ficará surpreso com quantas ferramentas do dia a dia usam alguma forma de inteligência artificial!"),
            },
            {
                "title": "🧠 Como a IA Aprende: Machine Learning",
                "body": [
                    "O coração da IA moderna é o Machine Learning (Aprendizado de Máquina). Em vez de seguir regras fixas programadas por humanos, os sistemas de ML aprendem a partir de dados — muitos dados.",
                    "Imagine ensinar uma criança a reconhecer gatos. Você não lista todas as regras ('tem bigodes, orelhas pontiagudas, ronrona...'). Em vez disso, você mostra centenas de fotos: 'isso é um gato, isso não é'. Com o tempo, ela aprende sozinha os padrões.",
                    "É exatamente assim que os algoritmos de ML funcionam. Alimentamos o sistema com exemplos, ele identifica padrões estatísticos, e aprende a fazer previsões sobre novos dados que nunca viu antes.",
                ],
                "tip": ("📊 Tipos de Aprendizado", "Supervisionado (aprende com exemplos rotulados), Não-supervisionado (encontra padrões sozinho) e Por Reforço (aprende com tentativa e erro — como treinar um cachorro com recompensas)."),
            },
            {
                "title": "🌊 Deep Learning e Redes Neurais",
                "body": [
                    "Se o Machine Learning é o motor da IA, o Deep Learning é o turbo. Inspirado no funcionamento do cérebro humano, utiliza redes neurais artificiais com múltiplas camadas (daí o 'deep', profundo) para aprender representações cada vez mais abstratas dos dados.",
                    "Foi o Deep Learning que possibilitou avanços surpreendentes: reconhecimento facial com precisão maior que humanos, tradução automática em tempo real e, mais recentemente, os modelos de linguagem como o ChatGPT.",
                    "Para você, estudante de ADS, entender esses conceitos não é só teoria: é a base para construir aplicações inteligentes que farão diferença no mercado de trabalho.",
                ],
                "tip": ("🚀 Por Onde Começar?", "Python é a linguagem da IA. Bibliotecas como NumPy, Pandas, Scikit-learn e TensorFlow são o kit básico de qualquer desenvolvedor de IA. E o melhor: tudo gratuito e open-source!"),
            },
        ]
    },
    {
        "num": "CAPÍTULO 02",
        "title": "Engenharia de Prompt",
        "sub": "A nova habilidade que todo profissional de tecnologia precisa dominar",
        "sections": [
            {
                "title": "✍️ O Que é Engenharia de Prompt?",
                "body": [
                    "Se os modelos de IA generativa são motores poderosos, os prompts são o volante. A Engenharia de Prompt é a arte e a ciência de formular instruções precisas para extrair o máximo valor dessas ferramentas.",
                    "Um prompt mal formulado gera respostas genéricas, imprecisas ou inúteis. Um prompt bem construído pode produzir conteúdo profissional, resolver problemas complexos e automatizar tarefas que tomariam horas.",
                    "Não é exagero dizer que Engenharia de Prompt se tornou uma das habilidades mais valorizadas no mercado tech em 2024-2025. Empresas estão contratando 'Prompt Engineers' com salários competitivos — e a barreira de entrada é surpreendentemente acessível.",
                ],
                "tip": ("🎯 A Regra de Ouro", "Quanto mais contexto você fornece ao modelo, melhor a resposta. Pense: quem é a IA neste contexto? O que ela deve fazer? Como deve responder? Para quem?"),
            },
            {
                "title": "🏗️ Estrutura de um Prompt Poderoso",
                "body": [
                    "Todo prompt eficaz contém quatro elementos fundamentais que funcionam em conjunto para guiar o modelo à resposta ideal.",
                    "PERSONA: Defina quem é a IA. 'Você é um professor universitário especialista em Python' gera respostas muito mais ricas do que simplesmente 'me explique Python'.",
                    "CONTEXTO: Forneça informações relevantes sobre a situação. Quanto mais específico você for, mais precisa será a resposta.",
                    "TAREFA: Seja explícito sobre o que você quer. Use verbos de ação: explique, liste, compare, crie, analise, resuma.",
                    "FORMATO: Especifique como quer a resposta: em bullet points, em tabela, com exemplos de código, em português formal, em no máximo 200 palavras.",
                ],
                "tip": ("📝 Técnica Few-Shot", "Dê exemplos do que você quer antes de fazer a pergunta. 'Aqui estão 2 exemplos do formato que preciso: [exemplo 1], [exemplo 2]. Agora crie um para [meu caso].'"),
            },
            {
                "title": "⚡ Técnicas Avançadas de Prompt",
                "body": [
                    "Chain-of-Thought (Cadeia de Pensamento): Peça à IA para 'pensar passo a passo' antes de responder. Isso melhora dramaticamente a qualidade em problemas que exigem raciocínio.",
                    "Role-Playing: Assuma papéis específicos nas conversas. 'Finja que você é um investidor cético e critique meu plano de negócios' traz perspectivas muito mais valiosas.",
                    "Self-Consistency: Peça múltiplas respostas para o mesmo problema e compare. 'Resolva este problema de 3 formas diferentes.' Depois escolha ou combine as melhores soluções.",
                    "Iteração e Refinamento: Raramente o primeiro prompt é perfeito. Trate a IA como um colaborador: 'Bom início, mas agora torne mais técnico e adicione exemplos de código em Python.'",
                ],
                "tip": ("🔄 Itere Sempre", "Os melhores resultados vêm de múltiplas iterações. Não desista no primeiro prompt — refine, ajuste o contexto, mude a persona e experimente formatos diferentes."),
            },
        ]
    },
    {
        "num": "CAPÍTULO 03",
        "title": "ChatGPT na Prática",
        "sub": "Casos de uso reais para estudantes e profissionais de tecnologia",
        "sections": [
            {
                "title": "💻 ChatGPT como Parceiro de Estudos",
                "body": [
                    "Para estudantes de ADS, o ChatGPT pode ser o tutor particular mais paciente e disponível que você já teve. Disponível 24h, nunca se irrita com perguntas 'básicas' e consegue explicar o mesmo conceito de dezenas de formas diferentes.",
                    "Debugging de Código: Cole seu código e a mensagem de erro. Peça ao ChatGPT para identificar o problema, explicar por que ocorreu e sugerir correções com explicação didática.",
                    "Entendendo Documentação: Documentações técnicas em inglês podem ser intimidadoras. Peça ao ChatGPT: 'Traduza e explique em linguagem simples esta documentação do React Hooks, com exemplos práticos.'",
                    "Preparação para Provas: 'Faça 10 questões de múltipla escolha sobre SQL avançado, no estilo de prova técnica de TI. Depois corrija minhas respostas com explicações detalhadas.'",
                ],
                "tip": ("📚 Prompt para Estudos", "'Explique [conceito] como se eu tivesse 15 anos, depois explique como se eu fosse um engenheiro sênior. Use exemplos do mundo real em cada versão.'"),
            },
            {
                "title": "🔧 ChatGPT para Desenvolvimento",
                "body": [
                    "A produtividade de desenvolvedores que usam IA generativa aumentou, em média, 55% segundo estudos da GitHub. Não é sobre substituir programadores — é sobre amplificar suas capacidades.",
                    "Geração de Código Boilerplate: 'Crie a estrutura completa de uma API REST em Node.js + Express com autenticação JWT, conexão ao MongoDB e tratamento de erros.' Em segundos você tem uma base sólida para trabalhar.",
                    "Code Review Automatizado: 'Analise este código Python e aponte: possíveis bugs, problemas de segurança, violações de boas práticas e sugestões de otimização de performance.'",
                    "Conversão entre Linguagens: 'Converta esta função JavaScript para Python, mantendo a mesma lógica e adicionando type hints.' Ideal para aprender novas linguagens comparando com o que você já conhece.",
                ],
                "tip": ("⚙️ Prompt de Desenvolvedor", "Sempre especifique: linguagem, versão, bibliotecas disponíveis e nível de detalhamento. 'Em Python 3.11, usando apenas bibliotecas padrão, sem frameworks externos.'"),
            },
            {
                "title": "📊 ChatGPT para Análise de Dados",
                "body": [
                    "Combinado com Python e bibliotecas como Pandas e Matplotlib, o ChatGPT se transforma em um poderoso assistente de análise de dados.",
                    "Interpretação de Resultados: Cole seus outputs do Pandas e peça uma análise narrativa. 'Estes são os resultados da minha análise. Escreva um parágrafo executivo explicando os principais insights para um gestor não técnico.'",
                    "Geração de Visualizações: 'Crie um código Python com Matplotlib para gerar um dashboard com 4 gráficos: evolução temporal, distribuição, correlação e top 10. Use paleta de cores profissional e adicione títulos descritivos.'",
                    "Limpeza de Dados: 'Aqui está uma amostra do meu dataset. Escreva um script Pandas para: tratar valores nulos, remover duplicatas, padronizar formatos de data e criar colunas derivadas úteis.'",
                ],
                "tip": ("📈 Dados + IA = Superpoder", "Aprenda SQL básico, Python com Pandas e o básico de visualização. Com essas três habilidades e o ChatGPT como copiloto, você se torna extremamente valioso no mercado de dados."),
            },
        ]
    },
    {
        "num": "CAPÍTULO 04",
        "title": "IA Generativa e o Futuro de TI",
        "sub": "Como se posicionar no mercado que está sendo redesenhado pela inteligência artificial",
        "sections": [
            {
                "title": "🌍 O Impacto Real da IA Generativa",
                "body": [
                    "Em 2023, o ChatGPT atingiu 100 milhões de usuários em apenas 2 meses — o produto de crescimento mais rápido da história. Em 2024, a IA generativa deixou de ser um diferencial e se tornou uma expectativa básica do mercado.",
                    "A pergunta já não é 'a IA vai impactar minha área?' mas sim 'como me posicionar para surfar essa onda em vez de ser engolido por ela?'",
                    "A boa notícia: a história mostra que novas tecnologias criam mais empregos do que destroem. A Revolução Industrial, a internet, os smartphones — cada onda tecnológica gerou profissões inexistentes antes. A IA não será diferente.",
                    "A diferença é a velocidade. O que levava décadas agora acontece em anos. Por isso, a habilidade mais importante do profissional moderno não é dominar uma tecnologia específica, mas a capacidade de aprender continuamente.",
                ],
                "tip": ("🎯 Posicionamento Estratégico", "Não compete com a IA — colabore com ela. As posições mais valorizadas serão as que combinam conhecimento técnico, criatividade humana e capacidade de orquestrar sistemas de IA."),
            },
            {
                "title": "💼 Carreiras em Alta na Era da IA",
                "body": [
                    "Prompt Engineer: Especialista em extrair o máximo dos modelos de IA. Salários iniciais nos EUA entre USD 100k-200k. No Brasil, demanda crescendo exponencialmente.",
                    "ML Engineer: Constrói e mantém sistemas de Machine Learning em produção. Combina habilidades de engenharia de software com conhecimento de ML. Um dos perfis mais escassos e bem pagos do mercado.",
                    "AI Product Manager: Gerencia produtos baseados em IA, traduzindo necessidades de negócio em soluções de IA. Exige tanto habilidades técnicas quanto de gestão e visão de produto.",
                    "Data Engineer com IA: Constrói os pipelines de dados que alimentam os sistemas de IA. A infraestrutura invisível que faz tudo funcionar. Altíssima demanda, baixa oferta de profissionais qualificados.",
                    "IA Ethics Officer: Garante que sistemas de IA sejam justos, transparentes e seguros. Perfil emergente com demanda crescente em grandes corporações e regulatórias.",
                ],
                "tip": ("🛤️ Seu Roadmap", "ADS → Python + SQL → Machine Learning básico → APIs de IA (OpenAI, Google, etc.) → Projetos no portfólio → GitHub ativo → LinkedIn estratégico. Cada passo conta!"),
            },
            {
                "title": "🛡️ IA Responsável e Ética",
                "body": [
                    "Com grande poder vem grande responsabilidade. Os profissionais de TI da nova geração precisam entender não só como construir com IA, mas quando não construir — e como fazê-lo de forma responsável.",
                    "Viés algorítmico é um problema real: sistemas de IA treinados com dados históricos podem perpetuar e amplificar discriminações existentes. Reconhecer e mitigar esses vieses é responsabilidade do desenvolvedor.",
                    "Transparência e explicabilidade: usuários têm o direito de entender por que um sistema de IA tomou uma decisão que os afeta. Construir sistemas que expliquem seus raciocínios é um diferencial ético e competitivo.",
                    "No Brasil, a Lei Geral de Proteção de Dados (LGPD) e as diretrizes emergentes de IA responsável do governo criam um contexto regulatório que todo profissional de TI precisa conhecer.",
                ],
                "tip": ("⚖️ Princípios de IA Responsável", "Fairness (equidade), Accountability (responsabilidade), Transparency (transparência) e Ethics (ética) — o acrônimo FATE resume os pilares da IA responsável. Incorpore-os desde o início dos seus projetos."),
            },
        ]
    },
    {
        "num": "CAPÍTULO 05",
        "title": "Seu Primeiro Projeto com IA",
        "sub": "Passo a passo para construir uma aplicação real com a API da OpenAI",
        "sections": [
            {
                "title": "🚀 Setup do Ambiente de Desenvolvimento",
                "body": [
                    "Vamos construir juntos um assistente inteligente usando Python e a API da OpenAI. Este é o tipo de projeto que fará diferença real no seu portfólio e nas suas entrevistas técnicas.",
                    "Primeiro, você precisará de uma conta na OpenAI (openai.com) e uma API Key. A conta gratuita oferece créditos suficientes para experimentar. Guarde sua chave com segredo — nunca a exponha em repositórios públicos.",
                    "Instale as dependências necessárias com pip install openai python-dotenv. A biblioteca openai fornece acesso à API, e python-dotenv gerencia suas variáveis de ambiente com segurança.",
                ],
                "tip": ("🔐 Segurança Primeiro", "NUNCA coloque sua API Key diretamente no código. Use um arquivo .env, adicione-o ao .gitignore e carregue com python-dotenv. Um arquivo .env exposto no GitHub pode gerar cobranças altíssimas."),
            },
            {
                "title": "⌨️ Seu Primeiro Código com a API",
                "body": [
                    "Aqui está a estrutura básica de uma chamada à API da OpenAI:",
                    "   from openai import OpenAI",
                    "   import os",
                    "   from dotenv import load_dotenv",
                    "   ",
                    "   load_dotenv()",
                    "   client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))",
                    "   ",
                    "   response = client.chat.completions.create(",
                    "     model='gpt-3.5-turbo',",
                    "     messages=[",
                    "       {'role': 'system', 'content': 'Você é um assistente útil.'},",
                    "       {'role': 'user', 'content': 'Olá! Como você funciona?'}",
                    "     ]",
                    "   )",
                    "   print(response.choices[0].message.content)",
                ],
                "tip": ("🎭 Os Três Papéis", "system: define a personalidade e regras da IA. user: é o que o usuário diz. assistant: são as respostas anteriores da IA. Mantenha o histórico para criar conversas com contexto persistente!"),
            },
            {
                "title": "🏆 Elevando seu Projeto ao Próximo Nível",
                "body": [
                    "Com o básico funcionando, é hora de adicionar funcionalidades que tornarão seu projeto memorável para recrutadores e colegas.",
                    "Memória de Conversa: Mantenha uma lista de mensagens e envie o histórico completo a cada nova chamada. Isso cria conversas coerentes onde a IA lembra do contexto anterior.",
                    "Interface Web: Use Flask ou FastAPI para criar uma API REST, depois conecte com uma interface HTML simples. Ou use Streamlit para criar dashboards de IA em Python puro em minutos.",
                    "System Prompt Personalizado: Crie uma persona única para sua IA. Um assistente focado em uma área específica, com um tom de voz característico e conhecimento especializado, impressiona muito mais que um chatbot genérico.",
                    "Documentação e README: Explique seu projeto, como rodar localmente, quais tecnologias usou e quais problemas ele resolve. Um README bem escrito é seu cartão de visitas no GitHub.",
                ],
                "tip": ("🌟 Diferencial de Portfólio", "Projetos que resolvem problemas REAIS se destacam. Pense: qual problema da sua vida, faculdade ou comunidade um assistente de IA poderia resolver? Construa isso — e conte essa história no seu LinkedIn!"),
            },
        ]
    },
]


# ── GERADOR PRINCIPAL ─────────────────────────────────────────────────────────
def build_ebook(output_path: str):
    styles = make_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=18*mm,
        title="IA na Prática — Do Zero ao Primeiro Projeto com ChatGPT",
        author="Thayná Batista da Silva",
        subject="Inteligência Artificial, ChatGPT, Engenharia de Prompt",
    )

    story = []
    avail_w = W - 40*mm

    # ── CAPA ─────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("IA na Prática", styles["cover_title"]))
    story.append(Spacer(1, 4*mm))
    story.append(GlowLine(avail_w * 0.6, C_CYAN))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Do Zero ao Primeiro Projeto com ChatGPT", styles["cover_subtitle"]))
    story.append(Spacer(1, 10*mm))

    # Decorative badge table
    badge_data = [["🤖 IA Generativa", "⚡ Engenharia de Prompt", "🐍 Python", "💬 ChatGPT"]]
    badge_table = Table(badge_data, colWidths=[avail_w/4]*4)
    badge_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_CARD),
        ("TEXTCOLOR", (0,0), (-1,-1), C_CYAN),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [C_CARD]),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LINEABOVE", (0,0), (-1,0), 1, C_BORDER),
        ("LINEBELOW", (0,-1), (-1,-1), 1, C_BORDER),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 50*mm))

    story.append(GlowLine(avail_w, C_BORDER))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Thayná Batista da Silva", styles["cover_author"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Análise e Desenvolvimento de Sistemas", styles["cover_meta"]))
    story.append(Paragraph("Faculdade Senac Recife-PE · Bootcamp Bradesco GenAI &amp; Dados — DIO 2026", styles["cover_meta"]))
    story.append(PageBreak())

    # ── SOBRE A AUTORA ────────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Sobre a Autora", styles["page_title"]))
    story.append(GlowLine(avail_w * 0.4, C_PURPLE))
    story.append(Spacer(1, 8*mm))

    about_data = [[
        Paragraph("👩‍💻", ParagraphStyle("icon", fontName="Helvetica-Bold", fontSize=40, textColor=C_PURPLE, alignment=TA_CENTER)),
        Paragraph(
            "<b>Thayná Batista da Silva</b><br/><br/>"
            "Estudante apaixonada por tecnologia, cursando Análise e Desenvolvimento de Sistemas "
            "na Faculdade Senac Recife-PE (turma 2025, formação prevista em 2027).<br/><br/>"
            "Participante do Bootcamp Bradesco — GenAI &amp; Dados na DIO, onde explorou "
            "Inteligência Artificial, Python para dados, IA Generativa, Power BI, SQL e "
            "Microsoft Copilot.<br/><br/>"
            "Acredita que a tecnologia é uma ferramenta de transformação social — e que "
            "qualquer pessoa, de qualquer origem, pode construir uma carreira sólida em TI "
            "com dedicação e os recursos certos.",
            ParagraphStyle("about_p", fontName="Helvetica", fontSize=10, textColor=C_WHITE, leading=17, alignment=TA_JUSTIFY)
        )
    ]]
    about_table = Table(about_data, colWidths=[35*mm, avail_w - 35*mm])
    about_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_CARD),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING", (0,0), (0,-1), 10),
        ("LEFTPADDING", (1,0), (1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ("ROUNDEDCORNERS", [8]),
        ("LINEABOVE", (0,0), (-1,0), 2, C_PURPLE),
    ]))
    story.append(about_table)
    story.append(Spacer(1, 8*mm))

    contact_data = [
        ["🔗 LinkedIn", "br.linkedin.com/in/thaynabds"],
        ["📷 Instagram", "@thaynabdstec"],
        ["📧 E-mail", "thaynabdstec@gmail.com"],
    ]
    ct = Table(contact_data, colWidths=[35*mm, avail_w - 35*mm])
    ct.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("TEXTCOLOR", (0,0), (0,-1), C_CYAN),
        ("TEXTCOLOR", (1,0), (1,-1), C_MUTED),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW", (0,0), (-1,-2), 0.5, C_BORDER),
    ]))
    story.append(ct)
    story.append(PageBreak())

    # ── SUMÁRIO ───────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Sumário", styles["page_title"]))
    story.append(GlowLine(avail_w * 0.4, C_CYAN))
    story.append(Spacer(1, 8*mm))

    toc_items = [
        ("01", "O Que é Inteligência Artificial", "Desmistificando a IA, ML e Deep Learning", "04"),
        ("02", "Engenharia de Prompt", "Como conversar com a IA de forma eficaz", "06"),
        ("03", "ChatGPT na Prática", "Casos de uso reais para estudantes e devs", "08"),
        ("04", "IA Generativa e o Futuro de TI", "Carreiras, ética e como se posicionar", "10"),
        ("05", "Seu Primeiro Projeto com IA", "Passo a passo com a API da OpenAI", "12"),
    ]
    for num, title, sub, pg in toc_items:
        toc_row = Table(
            [[
                Paragraph(f"<b>{num}</b>", ParagraphStyle("tnum", fontName="Helvetica-Bold", fontSize=14, textColor=C_PURPLE, alignment=TA_CENTER)),
                Paragraph(f"<b>{title}</b><br/><font color='#94A3B8' size='9'>{sub}</font>",
                          ParagraphStyle("titem", fontName="Helvetica", fontSize=11, textColor=C_WHITE, leading=17)),
                Paragraph(pg, ParagraphStyle("tpg", fontName="Helvetica-Bold", fontSize=12, textColor=C_CYAN, alignment=TA_CENTER)),
            ]],
            colWidths=[20*mm, avail_w - 38*mm, 18*mm]
        )
        toc_row.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), C_CARD),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("LEFTPADDING", (0,0), (0,-1), 8),
            ("RIGHTPADDING", (-1,0), (-1,-1), 8),
            ("LINEBELOW", (0,0), (-1,-1), 0.5, C_BORDER),
        ]))
        story.append(toc_row)
        story.append(Spacer(1, 3*mm))

    story.append(PageBreak())

    # ── CAPÍTULOS ─────────────────────────────────────────────────────────────
    for ch in CHAPTERS:
        story.append(Spacer(1, 4*mm))
        story.append(ChapterHeader(ch["num"], ch["title"], ch["sub"], avail_w))
        story.append(Spacer(1, 8*mm))

        for sec in ch["sections"]:
            story.append(Paragraph(sec["title"], styles["section_title"]))
            story.append(GlowLine(avail_w * 0.25, C_BORDER))
            story.append(Spacer(1, 4*mm))

            for para in sec["body"]:
                # Code lines
                if para.startswith("   "):
                    story.append(Paragraph(para.strip(), styles["code"]))
                else:
                    story.append(Paragraph(para, styles["body"]))

            story.append(Spacer(1, 4*mm))
            # Tip box
            tip_icon_title, tip_text = sec["tip"]
            story.append(TipBox("💡", tip_icon_title, tip_text, avail_w, styles))
            story.append(Spacer(1, 8*mm))

        story.append(PageBreak())

    # ── CONCLUSÃO ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Conclusão", styles["page_title"]))
    story.append(GlowLine(avail_w * 0.4, C_GREEN))
    story.append(Spacer(1, 8*mm))

    for p in [
        "Chegamos ao fim desta jornada — mas, na verdade, você está apenas no começo da maior revolução tecnológica da história. E a melhor parte: você já está se preparando para ela.",
        "A Inteligência Artificial não é um destino distante. É uma ferramenta poderosa que está disponível agora, que você pode começar a usar hoje, e que pode transformar radicalmente sua capacidade como desenvolvedor, analista e profissional de tecnologia.",
        "O que você aprendeu neste eBook é apenas a ponta do iceberg. Cada capítulo abre um universo de possibilidades: frameworks de ML, arquiteturas de LLMs, técnicas avançadas de prompt, aplicações específicas por área... há décadas de aprendizado apaixonante pela frente.",
        "Minha recomendação: comece agora. Abra o ChatGPT, experimente os prompts deste livro, crie sua conta na OpenAI, rode seu primeiro código de IA. A confiança vem com a prática — e cada projeto no seu portfólio é uma porta que se abre.",
        "Nos vemos no mercado! 💜",
    ]:
        story.append(Paragraph(p, styles["body"]))
        story.append(Spacer(1, 3*mm))

    story.append(Spacer(1, 12*mm))
    story.append(Paragraph('"A melhor hora para plantar uma árvore foi há 20 anos. A segunda melhor hora é agora."', styles["quote"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("— Provérbio Chinês", ParagraphStyle("attr", fontName="Helvetica", fontSize=10, textColor=C_MUTED, alignment=TA_CENTER)))
    story.append(PageBreak())

    # ── AGRADECIMENTOS ────────────────────────────────────────────────────────
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("Agradecimentos", styles["page_title"]))
    story.append(GlowLine(avail_w * 0.4, C_PURPLE))
    story.append(Spacer(1, 10*mm))

    story.append(Paragraph(
        "Este eBook é fruto de muito estudo, dedicação e do apoio de pessoas e comunidades incríveis. "
        "À DIO e ao Bradesco, por democratizarem o acesso à educação em tecnologia de ponta — "
        "vocês estão mudando vidas. Aos experts e mentores do bootcamp, pela generosidade em compartilhar "
        "conhecimento. À minha família, pelo suporte incondicional em cada hora de estudo. "
        "E a você, leitor, por investir no seu crescimento. Que este material seja apenas o primeiro "
        "passo de uma jornada incrível na tecnologia. 💜",
        styles["body"]
    ))
    story.append(Spacer(1, 10*mm))

    story.append(Paragraph("— Thayná Batista da Silva", ParagraphStyle(
        "sig", fontName="Helvetica-Oblique", fontSize=13, textColor=C_PURPLE_L, alignment=TA_CENTER)))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Recife-PE, 2026", ParagraphStyle(
        "city", fontName="Helvetica", fontSize=10, textColor=C_MUTED, alignment=TA_CENTER)))

    # ── BUILD ─────────────────────────────────────────────────────────────────
    # Use cover template for page 1, normal for rest
    doc.build(
        story,
        onFirstPage=make_page_template(is_cover=True),
        onLaterPages=make_page_template(is_cover=False),
    )
    print(f"✅ eBook gerado: {output_path}")


if __name__ == "__main__":
    out = "/mnt/user-data/outputs/ebook-ia-na-pratica.pdf"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build_ebook(out)
