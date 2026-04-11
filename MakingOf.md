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