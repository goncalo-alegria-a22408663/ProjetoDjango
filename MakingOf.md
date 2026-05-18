# Making Of — Modelação do Portfólio

**Autor:** Gonçalo Alegria (a22408663)
**Projeto Django — Programação Web**
**Curso:** Licenciatura em Engenharia Informática — Universidade Lusófona

---

## 1. Processo de modelação

A modelação foi feita em duas fases: primeiro no caderno (entidades, atributos, relações, DER e descrição dos modelos Django), depois implementação incremental em Django, modelo a modelo, com commits separados.

As fotos do trabalho em papel estão na pasta `media/makingof/`:

- `pagina1.jpeg` — Entidades 1, 2 e 3 (Licenciatura, UnidadeCurricular, Docente)
- `pagina2.jpeg` — Entidades 4, 5 e 6 (Projeto, Tecnologia, TFC)
- `pagina3.jpeg` — Entidades 7, 8 e 9 (Competencia, Formacao, MakingOf)
- `pagina4.jpeg` — Relações entre entidades e Diagrama Entidade-Relação (DER)
- `pagina5.jpeg` — Descrição dos modelos Django

---

## 2. Entidades modeladas

1. **Licenciatura** — cursos da Lusófona
2. **UnidadeCurricular** — UCs do plano de estudos
3. **Docente** *(entidade adicional)*
4. **Projeto** — projetos académicos
5. **Tecnologia** — linguagens, frameworks, ferramentas, BDs
6. **TFC** — trabalhos finais de curso
7. **Competencia** — competências técnicas, soft skills, linguísticas
8. **Formacao** — formações externas
9. **MakingOf** — documentação do processo

---

## 3. Decisões e justificações por entidade

### 3.1. Licenciatura

**Decisão 1 — `instituicao` como CharField (não entidade própria)**
Considerei extrair `Instituicao` como entidade própria com FK a partir de `Licenciatura` e `Formacao`. Decidi não o fazer porque, no contexto deste portfólio, todas as licenciaturas pertencem à Universidade Lusófona — criar uma entidade própria para um único valor seria sobre-engenharia desnecessária (princípio YAGNI).

**Decisão 2 — Manter o nome `Licenciatura` (e não generalizar para `Curso`)**
Após analisar o JSON dos TFCs, vi que existem TFCs de Mestrado e Doutoramento. Considerei renomear para `Curso`, mas optei por manter `Licenciatura` porque o portfólio é centrado no meu percurso de licenciatura. TFCs de outros graus são filtrados no carregamento.

---

### 3.2. UnidadeCurricular

**Decisão 1 — UC ↔ Licenciatura: Many-to-Many**
Uma UC pode pertencer a várias licenciaturas (ex: "Programação" aparece em LEI, LIG, etc.). Assumi que ano, semestre e ECTS são iguais em todas as licenciaturas onde a UC aparece, por isso esses atributos ficam na própria UC.

**Decisão 2 — UC ↔ Docente: Many-to-Many**
Uma UC pode ter vários docentes e um docente leciona várias UCs. Modelei como M:N para refletir esta realidade.

---

### 3.3. Docente *(entidade adicional)*

**Decisão 1 — Docente como entidade própria**
O enunciado pedia para "identificar os docentes associados", mas não obrigava a criar uma entidade. Optei por modelar como entidade independente para permitir normalização e atributos ricos. Esta é a **entidade adicional** exigida.

**Decisão 2 — Habilitação "Agregação" e uso de `choices`**
Adicionei "Agregação" às habilitações porque verifiquei no site oficial do DEISI que existe pelo menos um docente com esse grau. Usei `choices` para garantir consistência (evitar "Doutorado" vs "Doutoramento").

---

### 3.4. Projeto

**Decisão 1 — Projeto → UC: ForeignKey (1:N)**
Cada projeto foi feito no contexto de uma UC específica, por isso a relação é 1:N. Não faz sentido um projeto ser partilhado entre várias UCs.

**Decisão 2 — Projeto ↔ Tecnologia: Many-to-Many**
Um projeto usa várias tecnologias e uma tecnologia é usada em vários projetos. Esta relação permite navegação cruzada (ex: ver todos os projetos que usam Django).

---

### 3.5. Tecnologia

**Decisão 1 — Atributo `nivel_interesse`**
Pedido explicitamente pelo enunciado. Usei `IntegerField` com choices de 1 a 5 (escala simples e clara, com labels descritivos).

**Decisão 2 — `categoria` com choices**
Categorizei tecnologias em Linguagem / Framework / Ferramenta / Base de Dados, usando `choices` para consistência e para permitir filtros no Admin.

---

### 3.6. TFC

**Decisão 1 — TFC ↔ Licenciatura: Many-to-Many**
Após analisar o JSON real dos TFCs de 2025, confirmei que existem TFCs partilhados entre licenciaturas (ex: LEI + LIG). Por isso a relação é M:N.

**Decisão 2 — Modelado com base no JSON real**
Ajustei a entidade aos campos reais do JSON: `sumario` (em vez de `descricao`), `rating` (em vez de `nivel_interesse`), `palavras_chave`, `areas`, `tecnologias_usadas`, `link_pdf`, `imagem` como URLField. Mantive `areas`, `tecnologias_usadas` e `orientadores` como CharField (separados por `;`) por simplicidade.

---

### 3.7. Competencia

**Decisão 1 — Atributos `tipo` e `nivel` com choices**
Categorizei as competências em Técnica / Soft Skill / Linguística e níveis Básico / Intermédio / Avançado, usando `choices` para garantir consistência e permitir filtros.

**Decisão 2 — Entidade independente (não embutida em Tecnologia)**
Considerei colocar competências como atributo de Tecnologia, mas modelei como entidade própria porque competências também podem ser independentes de tecnologias (ex: "Trabalho em Equipa" é uma soft skill sem ligação direta a tecnologia).

---

### 3.8. Formacao

**Decisão 1 — `data_fim` opcional (`blank=True, null=True`)**
Uma formação pode estar em curso no momento do registo, por isso `data_fim` é opcional.

**Decisão 2 — Entidade isolada (sem relações obrigatórias)**
Optei por não criar relações M:N obrigatórias entre Formacao e Tecnologia/Competencia para manter a entidade simples. Caso seja necessário no futuro, é fácil acrescentar.

---

### 3.9. MakingOf

**Decisão 1 — M:N opcional para todas as entidades**
Em vez de uma única FK ou um campo de texto, modelei com M:N opcional (`blank=True`) para todas as entidades. Isto permite documentar decisões transversais e múltiplos MakingOfs por entidade ao longo do tempo.

**Decisão 2 — `blank=True` em todas as relações**
Sem `blank=True`, o Admin obrigaria a preencher as 8 relações em todos os registos, o que não faz sentido — um MakingOf documenta apenas algumas entidades, não todas.

---

### 3.10. Decisões transversais

**Ordem das classes em `models.py`**
As classes estão definidas pela ordem necessária para evitar erros de referência: independentes primeiro (Licenciatura, Docente, Competencia, Formacao), depois dependentes (UC, Tecnologia, TFC), depois Projeto, e por último MakingOf.

**Filtragem de TFCs no carregamento**
Dos 86 TFCs no JSON, 47 são de licenciatura e foram carregados; 37 são de Mestrado/Doutoramento e foram ignorados, coerentemente com a escolha de manter a entidade `Licenciatura`.

---

## 4. Erros encontrados e correções

### 4.1. Timeout no Codespace ao chamar a API da Lusófona
**Erro:** O script `load_curso_ucs` deu `ConnectTimeout` ao tentar chamar `secure.ensinolusofona.pt` a partir do GitHub Codespaces.

**Causa:** Os Codespaces do GitHub têm restrições de rede para domínios externos pouco comuns.

**Correção:** Descarreguei os JSONs no meu PC local (que tem acesso à API) e fiz upload para `data/lusofona/` no Codespace. Adaptei o script para ler dos ficheiros locais em vez de chamar a API diretamente.

### 4.2. Estrutura do JSON da API
**Erro:** O script inicial assumia campos como `curricularSemester` e `courseDescription`, mas os nomes reais no JSON são diferentes.

**Correção:** Inspecionei o JSON do curso para identificar os nomes corretos dos campos (`semesterCode`, `courseName`, etc.) e ajustei o script.

---

## 5. Uso de Inteligência Artificial

Utilizei o Claude como apoio durante o processo:

- **Modelação:** Usei o Claude para discutir alternativas de modelação (ex: M:N vs FK em UC↔Licenciatura, criar entidade Instituicao ou não, escolha de choices, etc.). Todas as decisões finais foram tomadas por mim, com base nas trocas de ideias.
- **Implementação:** Usei o Claude para validar o código dos modelos e do Admin, garantindo que estava correto e seguia as boas práticas.
- **Análise do JSON dos TFCs:** Após eu ter identificado que alguns TFCs pertencem a várias licenciaturas, o Claude ajudou-me a confirmar essa observação inspecionando a estrutura do JSON, o que reforçou a escolha M:N.
- **Debug:** O Claude ajudou-me a identificar a causa do timeout no Codespace e a alternativa de descarregar os JSONs localmente.
- **Documentação:** O Claude ajudou-me a estruturar e formatar o ficheiro MakingOf.md, deixando-o esteticamente organizado e legível.
- **Organização do trabalho:** Usei o Claude como uma checklist viva dos passos a seguir, confirmando o que já tinha feito e o que faltava, evitando repetir etapas ou perder tempo em coisas já concluídas.

---

## 6. Requisito adicional cumprido

A entidade adicional exigida pelo enunciado é a **`Docente`**, conforme justificado no ponto 3.2.

---

# Parte 2 — Ficha 7 (Views e Templates)

A Ficha 7 introduz a camada **View** e **Template** do padrão MVT do Django. O trabalho dividiu-se em duas partes: implementar de raiz uma aplicação simples para uma escola (exercício guiado), e depois aplicar o mesmo padrão ao portfólio (uma view, template e rota por cada modelo).

## 7. App `escola` (exercício guiado)

### 7.1. Estrutura da app

Criei uma nova app `escola` separada do `portfolio`, com três modelos: `Professor`, `Aluno` e `Curso`. As relações foram:

- `Curso → Professor` como ForeignKey (1:N): um curso tem um professor, um professor leciona vários cursos.
- `Curso ↔ Aluno` como ManyToManyField (M:N): um curso tem vários alunos, um aluno frequenta vários cursos.

Em ambas as relações usei `related_name='cursos'`, o que permite navegação reversa intuitiva: `professor.cursos.all()` e `aluno.cursos.all()`.

### 7.2. Implementação MVT

Para cada uma das três entidades (Curso, Professor, Aluno) implementei o ciclo completo: **view** em `views.py`, **template** em `templates/escola/`, e **rota** em `urls.py`. O template base (`base.html`) define o layout comum (header, nav, main com bloco `content`, footer) e os outros estendem-no.

### 7.3. Decisão — Otimização de queries

Em cada view, usei `select_related` ou `prefetch_related` para evitar o problema **N+1 queries**:

- **`select_related('professor')`** em `cursos_view`: faz um JOIN em SQL, ideal quando navego do lado da ForeignKey para o "pai" (curso → professor é 1).
- **`prefetch_related('alunos')`** em `cursos_view`: faz uma segunda query e junta em memória, necessário para relações M:N e reverse FK (curso → alunos pode ser N).
- **`prefetch_related('cursos')`** em `professores_view` e `alunos_view`: navego a reverse FK (`professor.cursos`) e a M:N reversa (`aluno.cursos`), ambas potencialmente N — por isso `select_related` não serve aqui.

### 7.4. Decisão — Estrutura HTML5 semântica

Usei elementos semânticos (`section`, `article`, `header`, `nav`, `main`, `footer`) em vez de `div` genéricos. Isto facilitou a estilização (o CSS pode atacar `article > header > h3` sem precisar de classes) e tornou a marcação reutilizável: o `cursos.html`, `professores.html` e `alunos.html` partilham exatamente a mesma estrutura (`<section>` → `<article>` → `<header>` + `<section>` interno), pelo que o mesmo CSS estiliza as três páginas.

### 7.5. Decisão — Página de detalhe de um curso

Implementei uma rota parametrizada `path('curso/<int:id>', ...)` que recebe o `id` do curso e mostra uma página de detalhe com a imagem, professor e alunos. Os links foram colocados a partir da página de alunos (cada curso na lista de cursos do aluno é clicável), seguindo o enunciado.

### 7.6. Decisão — Não estender link clicável ao `professores.html`

Considerei aplicar o mesmo padrão de link clicável também na lista de cursos dos professores, para consistência de navegação. No fim optei por seguir o enunciado à letra, que só pede os links na página de alunos. Decisão pragmática: priorizar conformidade ao enunciado sobre uniformidade visual.

### 7.7. Decisão — Melhoria das rotas (raiz no escola)

A ficha sugere uma "melhoria" em que o `/` da aplicação aponta para a app escola, evitando o prefixo `/escola/`. Aceitei a sugestão da ficha mesmo sabendo que, num projeto com múltiplas apps (escola + portfolio), faria mais sentido a raiz pertencer ao portfólio. A escolha foi seguir o enunciado; se em fichas futuras for pedido para a raiz apontar para o portfólio, esta configuração será revista.

### 7.8. Estilização

Criei `escola/static/escola/styles.css` baseado no exemplo da ficha, com layout em cards (background branco, cantos arredondados, sombra subtil), header e footer escuros, e elementos da lista renderizados como "pills" azuis arredondadas. Configurei `STATIC_ROOT` no `settings.py` e corri `collectstatic`. O CSS depende inteiramente da estrutura HTML semântica (seletores CSS sem classes), o que se provou ser uma decisão acertada na Parte 2 quando reaproveitei o mesmo CSS no portfólio.

---

## 8. Views do Portfólio

Após terminar a app escola, apliquei o mesmo padrão ao portfólio: para cada um dos 9 modelos (`Licenciatura`, `Docente`, `UnidadeCurricular`, `Competencia`, `Tecnologia`, `TFC`, `Projeto`, `Formacao`, `MakingOf`) criei uma **view** de listagem, um **template** e uma **rota**.

### 8.1. Decisão — Reaproveitamento da estrutura HTML e CSS

Copiei o `styles.css` e a estrutura HTML do template `base.html` da app escola para a app portfolio (`portfolio/static/portfolio/styles.css` e `portfolio/templates/portfolio/base.html`). Como os templates de cada modelo seguem a mesma estrutura semântica (`<section>` → `<article>` → `<header>` + `<section>` interno), o CSS funciona sem alterações.

### 8.2. Decisão — Apenas listagens (sem páginas de detalhe)

O enunciado pede "uma view, um template e a respetiva URL para cada classe". Interpretei isto como uma listagem por modelo, sem páginas de detalhe (que apenas a app escola implementa, como exemplo). Esta decisão mantém o esforço alinhado com o pedido e deixa espaço para fichas futuras estenderem o trabalho.

### 8.3. Decisão — Otimização de queries por modelo

Apliquei `select_related` e `prefetch_related` consoante a estrutura de relações de cada modelo:

- **Sem relações no template** (`Licenciatura`, `Docente`, `Competencia`, `Formacao`): nenhum prefetch.
- **M:N**: `prefetch_related` (`Tecnologia.competencias`, `UC.licenciaturas`/`docentes`, `TFC.licenciaturas`).
- **FK + M:N** (`Projeto`): `select_related('unidade_curricular')` + `prefetch_related('tecnologias')`.
- **M:N múltiplas** (`MakingOf`): `prefetch_related` de todas as 8 relações em simultâneo.

### 8.4. Decisão — Campos mostrados em cada card

Para cada modelo escolhi os campos mais informativos numa listagem: tipicamente nome/título e tipo/categoria no `<header>`, e relações ou metadados na `<section>` interna. Para `Docente`, `Tecnologia` e `Competencia` usei os métodos `get_<campo>_display()` para obter o label legível dos `choices` (ex: "Doutoramento" em vez de "DOUT").

### 8.5. Estrutura de URLs

Todas as rotas do portfólio ficam sob o prefixo `/portfolio/` (configurado no `project/urls.py` com `include('portfolio.urls')`). As 9 rotas seguem o padrão `path('nome_plural/', views.nome_plural_view, name="nome_plural")`.

---

## 9. Uso de Inteligência Artificial (Ficha 7)

Continuei a usar o Claude como apoio, no mesmo espírito da Ficha 6:

- **Modelação conceptual:** Discuti com o Claude qual a diferença entre `select_related` e `prefetch_related`, e quando aplicar cada um. Validei o meu raciocínio para cada view do portfólio antes de implementar.
- **Debug:** O Claude ajudou a diagnosticar erros como `NameError: include is not defined`, `ModuleNotFoundError: escola.urls`, e gralhas em templates (ex: `{% for x in y}` sem `%`).
- **Mensagens de commit:** Pedi ao Claude para gerar mensagens de commit descritivas a cada passo, mantendo o histórico legível.

---

# Parte 3 — Ficha 8 (Forms / CRUD / Página "Sobre")

A Ficha 8 introduz **formulários** em Django, permitindo operações **CRUD** (Create, Read, Update, Delete) através do browser sem passar pelo admin. Também inclui a criação de uma página "Sobre esta Aplicação" que documenta o projeto.

## 10. Formulários CRUD

### 10.1. Decisão — Modelos com CRUD implementado

A ficha pediu CRUD em quatro modelos: `Projeto`, `Tecnologia`, `Competencia` e `Formacao`. Implementei os quatro seguindo o mesmo padrão.

### 10.2. Padrão de implementação

Para cada modelo, o ciclo de implementação foi:

1. **ModelForm** em `portfolio/forms.py` — classe com `Meta` que aponta para o modelo e usa `fields = '__all__'` para incluir todos os campos.
2. **Três views** em `portfolio/views.py`: `novo_X_view`, `edita_X_view` e `apaga_X_view`.
3. **Três rotas** em `portfolio/urls.py`: `X/novo/`, `X/<int:X_id>/edita` e `X/<int:X_id>/apaga`.
4. **Dois templates** por modelo: `novo_X.html` e `edita_X.html`. Não foi criado template de confirmação para o `apaga` — segue o estilo do exemplo da biblioteca apresentado em aula.
5. **Botões** na página de listagem: um botão "Inserir novo X" no topo, e botões "Editar" / "Apagar" em cada card.

### 10.3. Decisão — Estilo das views (alinhamento com o exemplo do professor)

Adotei a nomenclatura do exemplo da biblioteca apresentado em aula (`novo_X_view`, `edita_X_view`, `apaga_X_view`) em vez do estilo mais comum em Django (`X_create`, `X_update`, `X_delete`). Razões: consistência com o material da disciplina e facilidade de avaliação pelo docente.

Para o controlo de fluxo nas views, usei o padrão `form = X(request.POST or None, request.FILES)` seguido de `if form.is_valid():` — mais conciso que o `if request.method == 'POST': ... else: ...` tradicional, e é o que o exemplo da biblioteca usa.

### 10.4. Decisão — Apagar sem confirmação

Considerei adicionar uma página de confirmação antes de apagar registos (boa prática para evitar perdas acidentais), mas optei por seguir o padrão da ficha: clicar em "Apagar" remove o registo imediatamente. Em produção esta decisão seria revista; aqui mantém a fidelidade ao enunciado.

### 10.5. Decisão — Widgets para datas

Em `ProjetoForm` e `FormacaoForm`, usei `forms.DateInput(attrs={'type': 'date'})` para forçar o input HTML5 nativo de data em vez do input de texto por defeito do Django. Melhora a UX e evita problemas de formato.

### 10.6. Erro encontrado — CSRF no Codespace

Ao submeter os primeiros formulários, o Django devolveu `403 Forbidden — CSRF verification failed`. A causa foi o port-forwarding do GitHub Codespaces: o browser acede via `https://*.app.github.dev` mas o Django recebe o pedido com `Origin: https://localhost:8000`. Esta origem não estava na lista de origens confiáveis.

**Correção:** adicionei em `settings.py`:

```python
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.app.github.dev',
    'https://localhost:8000',
    'http://localhost:8000',
]
```

### 10.7. Erro encontrado — Template em falta

Ao testar o CRUD de Competências, descobri que o template `competencias.html` não tinha sido criado na Ficha 7 (apesar de a view e rota existirem). Era um bug silencioso porque o link no nav também estava em falta, e por isso nunca tinha visitado a página. Criei o template e adicionei o link no nav.

### 10.8. Estilização — botões e formulários

Adicionei regras CSS específicas para `<button>`, `<input>`, `<textarea>`, `<select>` e `<form table>`. Mantive o vocabulário visual da app (pills arredondadas, azul `#2563eb` como cor de destaque), criando um botão primário azul para ações principais ("Inserir novo X", "Submit") e botões secundários neutros para ações secundárias ("Editar", "Cancelar").

## 11. Página "Sobre esta Aplicação"

### 11.1. Estrutura

A página agrega 6 secções: arquitetura MVT, modelação, tecnologias, estrutura de páginas, repositório GitHub e Making Of. Foi implementada como uma única view (`sobre_view`) com template estático para as secções narrativas, e conteúdo dinâmico nas secções 3 e 6.

### 11.2. Decisão — Classe `Tipo` (nova entidade)

A ficha pediu para "agrupar as tecnologias em tipos: frontend, backend, base de dados, storage, outros" e explicitamente para "criar uma classe para tipo e incluir nas tecnologias". Implementei como `ForeignKey` em `Tecnologia` (1:N — uma tecnologia pertence a um tipo, um tipo agrupa várias tecnologias).

Usei `on_delete=models.SET_NULL` com `null=True, blank=True` para que apagar um tipo não apague as tecnologias associadas (apenas as deixa sem tipo). Esta opção é mais segura que `CASCADE` ou `PROTECT` para este caso.

Considerei usar `choices` (como em `Tecnologia.categoria` ou `Docente.habilitacao`), mas a ficha pediu explicitamente uma **classe** — o que permite no futuro adicionar atributos ao Tipo (descrição, ordenação, etc.) sem alterar a `Tecnologia`.

### 11.3. Decisão — Markdownify para o Making Of

Para a secção 6, usei o módulo `django-markdownify` para renderizar o ficheiro `MakingOf.md` diretamente como HTML formatado. A alternativa seria copiar o conteúdo para o template ou listar registos do modelo `MakingOf` da base de dados.

**Vantagens da abordagem escolhida:**
- O `MakingOf.md` continua a ser o único ficheiro fonte da documentação (não há duplicação)
- Renderização automática a cada alteração — basta editar o `.md` e a página atualiza
- Mantém formatação Markdown rica (cabeçalhos, listas, código, tabelas)

**Configuração:** adicionei `markdownify.apps.MarkdownifyConfig` aos `INSTALLED_APPS` e configurei `MARKDOWNIFY['default']['WHITELIST_TAGS']` com os elementos HTML necessários para renderizar o documento completo, incluindo `code`, `pre`, `hr`, `br`, e elementos de tabela. Adicionei as extensões `fenced_code` e `tables` para suporte de blocos de código e tabelas Markdown.

### 11.4. Erro encontrado — `TemplateSyntaxError` por sintaxe Django no template

Na secção 1 (explicação do MVT), incluí no texto descritivo os símbolos `{{ }}` e `{% %}` para explicar a linguagem de templates. O Django interpretou esses símbolos como sintaxe de templates real e devolveu `Empty variable tag`.

**Correção:** envolver esses símbolos em `{% verbatim %}{% endverbatim %}` para o Django os tratar como texto literal.

## 12. Uso de Inteligência Artificial (Ficha 8)

Continuei a usar o Claude como apoio. Notas relevantes desta ficha:

- **CRUD modelo a modelo:** após implementar o primeiro modelo (Projeto) com o Claude a explicar cada passo, os restantes três (Tecnologia, Competencia, Formacao) foram pedidos em "modo despachar" — pedi código completo de uma vez. Ressalvas pessoais: revi cada bloco antes de aplicar, sobretudo os widgets e os imports, para garantir que ficavam alinhados com os meus modelos.
- **Comparação com o exemplo da biblioteca:** colei o README do `bibliotecalusofona` na conversa para o Claude alinhar a nomenclatura e estilo do código com o exemplo do professor (uso de `request.POST or None`, nomes de funções `novo_X_view`, etc.).
- **Debug:** o Claude ajudou a diagnosticar o erro de CSRF no Codespace e a explicar o porquê do port-forwarding interagir mal com o `CSRF_TRUSTED_ORIGINS`, bem como o erro de indentação na classe `Tipo` e o `NameError` quando coloquei a classe na ordem errada.
- **Mensagens de commit:** mantive a prática de pedir mensagens de commit no fim de cada bloco funcional.