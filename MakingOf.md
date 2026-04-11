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

## 3. Decisões e justificações

### 3.1. UC ↔ Licenciatura: Many-to-Many
Uma UC pode pertencer a várias licenciaturas (ex: "Programação" aparece em LEI, LIG, etc.). Assumi que ano, semestre e ECTS são iguais em todas as licenciaturas onde a UC aparece, por isso esses atributos ficam na própria UC e não numa tabela intermédia. Caso esta premissa deixe de ser válida, seria necessário introduzir uma entidade intermédia `UCnoCurso` com `through=`.

### 3.2. Docente como entidade própria (entidade adicional)
O enunciado pedia para "identificar os docentes associados" às UCs, mas não obrigava a criar uma entidade própria — poderia ter sido resolvido com um simples CharField. Optei por modelar `Docente` como entidade independente porque:
- Permite normalização (um docente leciona várias UCs sem duplicação de dados)
- Permite armazenar atributos ricos como habilitação académica e regime de contrato (informação pública no site oficial do DEISI)
- Facilita futuras extensões (orientadores de TFCs, projetos, etc.)

Esta é a minha **entidade adicional** exigida pelo requisito do enunciado.

### 3.3. Uso de `choices` em vez de texto livre
Em `Docente.habilitacao`, `Docente.regime_contrato`, `Tecnologia.categoria`, `Competencia.tipo` e `Competencia.nivel` usei `choices` para garantir consistência dos dados (evitar valores inconsistentes como "Doutorado" vs "Doutoramento") e para o Admin gerar dropdowns automaticamente, facilitando filtros.

### 3.4. Habilitação "Agregação"
Adicionei "Agregação" às habilitações dos docentes porque verifiquei no site oficial do DEISI que existe pelo menos um docente com esse grau (Aleksandar Mikovic).

### 3.5. `instituicao` como CharField (não entidade própria)
Considerei extrair `Instituicao` como entidade própria com FK a partir de `Licenciatura` e `Formacao`, para melhor normalização. Decidi não o fazer porque, no contexto deste portfólio, todas as licenciaturas pertencem à Universidade Lusófona — criar uma entidade própria para um único valor seria sobre-engenharia desnecessária (princípio YAGNI). Caso o portfólio venha a incluir formações de outras instituições no futuro, esta decisão pode ser facilmente revertida.

### 3.6. MakingOf com M:N opcional para todas as entidades
Em vez de uma única ForeignKey ou um campo de texto a indicar a entidade documentada, modelei `MakingOf` com `ManyToManyField` opcional (`blank=True`) para todas as entidades. Isto permite:
- Um mesmo registo de Making Of documentar decisões transversais que afetam várias entidades simultaneamente
- Cada entidade ter vários Making Ofs ao longo do tempo, refletindo a evolução do modelo

Esta abordagem está alinhada com a indicação do enunciado de que "esta informação deverá estar estruturada e relacionada, sempre que fizer sentido, com outras entidades".

### 3.7. Tecnologia com `nivel_interesse`
Pedido explicitamente pelo enunciado, para representar o meu nível de interesse/preferência por cada tecnologia. Usei `IntegerField` com choices de 1 a 5 (escala simples e clara, com labels descritivos).

### 3.8. Projeto com FK para UC (1:N)
Cada projeto foi feito no contexto de uma UC específica, por isso a relação é 1:N (um projeto pertence a uma UC; uma UC pode ter vários projetos). Não faz sentido um projeto ser partilhado entre várias UCs.

### 3.9. TFC ↔ Licenciatura: Many-to-Many
Inicialmente considerei FK, mas após analisar o ficheiro JSON real dos TFCs de 2025, confirmei que existem TFCs que pertencem a mais que uma licenciatura (ex: um TFC partilhado entre LEI e LIG). Por isso a relação é M:N.

### 3.10. TFC modelado com base no JSON real
Após analisar o ficheiro `tfcs_2025.json`, ajustei a entidade TFC à estrutura real dos dados:
- Adicionei campos que existiam no JSON: `palavras_chave`, `areas`, `tecnologias_usadas`, `link_pdf`, `imagem`, `orientadores`
- Renomeei `descricao` → `sumario` e `nivel_interesse` → `rating` para refletir os nomes do JSON
- `imagem` é `URLField` (não `ImageField`) porque o JSON tem URLs externas em vez de ficheiros para upload

### 3.11. Áreas, tecnologias e orientadores em TFC como CharField
Considerei criar entidades próprias e relações M:N para `areas`, `tecnologias_usadas` e `orientadores` em TFC, mas optei por mantê-los como `CharField` (separados por `;`) por simplicidade. As relações ricas com tecnologias existem para a entidade `Projeto`, que é onde fazem mais sentido para o meu portfólio pessoal.

### 3.12. Filtragem de TFCs no carregamento
O script `load_tfcs` filtra apenas TFCs de licenciatura. Dos 86 TFCs no JSON, 47 são de licenciatura e foram carregados; 37 são de Mestrado/Doutoramento ou têm o campo `licenciaturas` vazio e foram ignorados. Esta decisão é coerente com a escolha de manter a entidade chamada `Licenciatura` em vez de a generalizar para `Curso`.

### 3.13. Carregamento das UCs via API da Lusófona
O carregamento das UCs do curso de LEI é feito a partir dos JSONs descarregados da API oficial da Lusófona (`secure.ensinolusofona.pt`), guardados em `data/lusofona/`. O script `load_curso_ucs` lê o ficheiro do curso e cada ficheiro de UC, criando os registos correspondentes na BD. Os JSONs originais contêm muito mais informação (bibliografia, métodos de avaliação, horários, etc.) — armazenei apenas os campos relevantes para o portfólio (nome, código, ano, semestre, ECTS, descrição), mantendo os ficheiros originais para futura expansão.

### 3.14. Ordem das classes em models.py
As classes estão definidas pela ordem necessária para evitar erros de referência: primeiro as independentes (`Licenciatura`, `Docente`, `Competencia`, `Formacao`), depois as dependentes (`UnidadeCurricular`, `Tecnologia`, `TFC`), depois `Projeto`, e por último `MakingOf`. Uma classe só pode referenciar outra que já tenha sido definida acima.

### 3.15. `blank=True` nas relações do MakingOf
Todas as relações M:N do `MakingOf` têm `blank=True` porque são opcionais por natureza — um Making Of documenta apenas algumas entidades, não todas. Sem `blank=True`, o Admin obrigaria a preencher as 8 relações em todos os registos.

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

---

## 6. Requisito adicional cumprido

A entidade adicional exigida pelo enunciado é a **`Docente`**, conforme justificado no ponto 3.2.