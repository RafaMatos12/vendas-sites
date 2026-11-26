# Coleta no Google Maps / Google Meu Negócio

Tudo pelo navegador embutido, lendo a página pública como um usuário. Uma empresa por vez.

## 1. Encontrar o perfil

1. Abrir `https://www.google.com/maps/search/<nome da empresa> <cidade> SC` (espaços como `+`).
2. Se abrir uma **lista**, usar `get_page_text`/`find` para ver nome + endereço de cada resultado:
   - um resultado claramente certo → clicar nele;
   - vários plausíveis ou nenhum → **parar e perguntar** ao Rafael.
3. Com o perfil aberto, guardar a URL atual em `empresa.maps_url`.

Se aparecer banner de cookies/consentimento, escolher a opção que **recusa** o não essencial.

## 2. Dados do perfil (aba "Visão geral")

Ler com `get_page_text` e conferir com `find` quando estiver ambíguo:

| Campo | Para `site.json` |
|---|---|
| Nome oficial | `empresa.nome` |
| Categoria (ex.: "Padaria") | `empresa.segmento` e `schema_tipo` (ver tabela abaixo) |
| Endereço completo | `empresa.endereco` e `empresa.maps_consulta` |
| Telefone | `empresa.telefone`; se for celular (9 dígitos), usar também como `empresa.whatsapp` |
| Horários (expandir a lista) | `empresa.horarios`, agrupando dias iguais ("Segunda a sexta") |
| Site atual, se houver | anotar: argumento de venda ("o site de vocês está fora do ar/desatualizado") |
| Nota e nº de avaliações | `avaliacoes.nota` e `avaliacoes.total` |
| "Sobre"/atributos (ex.: "Entrega", "Wi-Fi", "Acessível") | ideias para `faixa` e `sobre.destaques` |
| Link **"Reivindicar esta empresa"** | o dono não gerencia o perfil: argumento de venda, e as fotos são todas de clientes (avisar no checkpoint) |
| Frases do "Resumo de avaliações" | bons candidatos para `faixa` e para o subtítulo do hero |

Sem login no Google, o Maps mostra "visualização limitada": aparecem dados, ~3 avaliações e poucas fotos. Se precisar de mais avaliações ou fotos, pedir ao Rafael para entrar na conta Google no painel do navegador (opcional).

## 3. Avaliações (aba "Avaliações")

- Ordenar por **Mais relevantes**. Ler as ~20 primeiras com `get_page_text`. Se houver "Mais", expandir só as que interessam.
- Escolher **3–6** avaliações de 5 estrelas que citem coisas **concretas** (um produto, o atendimento de alguém, o ambiente). Elas também alimentam a `faixa` e os textos.
- Autor: primeiro nome e inicial do sobrenome ("Maria S."). Nunca o nome completo nem a foto.
- Anotar também elogios recorrentes (eles viram diferenciais) e reclamações recorrentes (não usar no site, mas citar no checkpoint como contexto de venda).

## 4. Fotos (aba "Fotos")

1. Preferir a sub-aba **"Do proprietário"** (ou "By owner"). Depois "Vídeos/Interior/Comida" etc.
2. Para pegar as URLs, usar `read_page`/`find` nas imagens, ou `javascript_tool` **só para inspecionar**, por exemplo:
   ```js
   [...new Set([...document.querySelectorAll('img')].map(i => i.src)
     .filter(s => /googleusercontent\.com\/(grass-cs|gps-cs|p)\//.test(s)))].slice(0, 40)
   ```
   **Nunca** usar URLs com `/a-/` ou `/a/`: são fotos de perfil de quem avaliou (dado pessoal). Fotos do local ficam em `/grass-cs/`, `/gps-cs/` ou `/p/`. Testado em 26/11/2026: `imagens.py` baixa essas URLs na resolução original (~1080px).
   As fotos de fundo às vezes vêm em `style="background-image:url(...)"`. Nesse caso, ler o atributo `style` dos elementos.
3. Abrir algumas fotos para julgar a qualidade. Escolher fachada, ambiente, produtos e equipe. Descartar fotos escuras, tortas ou com clientes em primeiro plano.
4. Pôr as escolhidas no `lista-imagens.txt`. O `imagens.py` já troca o sufixo de tamanho do Google por `=w1600`.

## 5. Tipo schema.org (`schema_tipo`)

| Categoria no Google | `schema_tipo` |
|---|---|
| Padaria, confeitaria | `Bakery` |
| Restaurante, lanchonete, pizzaria | `Restaurant` |
| Cafeteria | `CafeOrCoffeeShop` |
| Salão, barbearia, estética | `BeautySalon` / `HairSalon` |
| Oficina mecânica | `AutoRepair` |
| Loja (roupa, presentes etc.) | `Store` / `ClothingStore` |
| Clínica, consultório | `MedicalClinic` / `Dentist` |
| Academia | `ExerciseGym` |
| Pet shop | `PetStore` |
| Outros | `LocalBusiness` |

## Se o Google bloquear ou pedir verificação

Não tentar contornar. Não resolver CAPTCHA. Parar, avisar o Rafael e seguir só com o que ele informar ou com o que o Instagram mostrar.
