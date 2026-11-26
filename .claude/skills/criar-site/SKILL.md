---
name: criar-site
description: Cria o site one-page de um estabelecimento local (Videira e região) para venda por cold call e entrega pronto no localhost. Use quando o Rafael passar o nome de uma empresa (e cidade) e pedir para criar/fazer o site, ou digitar /criar-site. Coleta dados no Google Maps/Meu Negócio e Instagram, define o tom de voz, busca referência de estrutura no Pinterest, gera o site com efeitos e devolve só o link do localhost. Publica (GitHub privado + Vercel) apenas quando o Rafael pedir "publicar".
---

# /criar-site — do nome da empresa ao site pronto no localhost

O papel do Rafael é **dizer a empresa e fornecer dados extras**. Todo o resto é desta skill. A entrega é o **site finalizado + o link do localhost**. Publicar é um segundo comando, só quando ele pedir.

## Modo silencioso (obrigatório)

Para economizar tokens:

- **Não narrar** o que está fazendo, nem antes nem entre as ferramentas. Nada de "agora vou…", resumos de etapa ou explicação de decisões.
- Não tirar screenshots só para mostrar; usar `read_page`/`get_page_text`/`javascript_tool` para conferir, e screenshot apenas se precisar enxergar um problema visual.
- Não usar `update_plan` nem `wrap_up` durante a skill.
- Só falar com o Rafael em dois casos: **bloqueio** (empresa ambígua/não encontrada, login necessário) com uma pergunta curta, ou a **entrega final** no formato do Passo 6.

Entrada típica: `/criar-site Padaria Bom Gosto, Videira` (opcional: @instagram, telefone, observações da ligação).

Caminhos (relativos à raiz do workspace `Documents\VendasSites`):

| O quê | Onde |
|---|---|
| Scripts | `.claude/skills/criar-site/scripts/` (`render.py`, `imagens.py`, `verificar.py`, `publicar.py`) |
| Template base | `.claude/skills/criar-site/template/` (`styles.css`, `main.js`) |
| Exemplo completo de `site.json` | `.claude/skills/criar-site/references/site.exemplo.json` |
| Cada site | `sites/<slug>/` — vira o repositório `<slug>` no GitHub |
| Controle de vendas | `sites/_controle.md` |

Rodar Python sempre com o ambiente do workspace: `.venv/Scripts/python.exe -I` (tem o Pillow). Se `.venv` não existir: `python -m venv .venv` e depois `.venv/Scripts/python.exe -m pip install pillow`. Slug: `<nome-da-empresa>-<cidade>` em minúsculas com hífen, sem acento (ex.: `padaria-bom-gosto-videira`).

---

## Passo 0 — Preparar

1. Criar `sites/<slug>/`. Se já existir, é **atualização**: ler o `site.json` existente e perguntar o que muda.
2. Abrir o navegador embutido (`mcp__Claude_Browser__*`). Ler `references/coleta-google.md`, `references/analise-instagram.md` e `references/referencia-pinterest.md` antes das etapas correspondentes.

## Passo 1 — Google Maps / Meu Negócio

Seguir `references/coleta-google.md`. Resultado: o bloco `empresa` + `avaliacoes` do `site.json` e a lista de fotos candidatas.

- Se aparecer **mais de um estabelecimento** com o nome, ou nenhum: **parar e perguntar** qual é (mostrar nome + endereço de cada).
- Telefone fixo sem indicação de WhatsApp → anotar e perguntar no checkpoint (o Rafael confirma na ligação).

## Passo 2 — Instagram

Seguir `references/analise-instagram.md`. Resultado: `tema.tom`, cores, `efeitos`, textos com a voz da empresa e fotos candidatas.

- Sem Instagram encontrado: inferir o tom pelo segmento e pelas avaliações, e dizer isso no checkpoint.
- Se pedir login: pedir ao Rafael para entrar no painel do navegador. **Nunca digitar senha.**

## Passo 3 — Referência no Pinterest

Seguir `references/referencia-pinterest.md`. Resultado: 2–3 links de referência, a variante do hero (`split`, `imagem-cheia` ou `centralizado`), a ordem das seções e os ajustes que vão para `custom.css`.

Pinterest é **inspiração de estrutura** (ordem das seções, ritmo, composição). Não copiar o visual, os textos nem as imagens de um site específico.

## Passo 4 — Montar o site

1. **Imagens:** escrever `sites/<slug>/lista-imagens.txt` (`nome origem` por linha) e rodar
   `.venv/Scripts/python.exe -I .claude/skills/criar-site/scripts/imagens.py sites/<slug> sites/<slug>/lista-imagens.txt`.
   Prioridade de fonte: fotos do **proprietário** no Google > posts do Instagram da empresa > fotos de clientes no Google (último caso, e avisar no checkpoint). 6–10 fotos bastam. Não usar foto onde apareça rosto de cliente em destaque.
2. **site.json:** escrever `sites/<slug>/site.json` seguindo `references/site.exemplo.json`. Textos:
   - Na **voz da empresa** (tom do Passo 2), em português do Brasil, curtos e concretos. Nada genérico do tipo "qualidade e excelência".
   - Usar só fatos coletados. Não inventar prêmios, anos de mercado, números ou serviços. Se faltar algo, a seção sai mais curta.
   - Avaliações em destaque: trechos **reais** do Google, com o primeiro nome do autor e a inicial do sobrenome. Cortar com "…" se for longo.
   - `demo: true` sempre (site fica fora do Google até a venda).
   - `faixa`: 4–6 diferenciais curtos tirados das avaliações e do Instagram.
3. **Render:** `.venv/Scripts/python.exe -I .claude/skills/criar-site/scripts/render.py sites/<slug>`
4. **custom.css:** aplicar os ajustes da referência do Pinterest e do tom (ex.: hero com fundo de cor, títulos em caixa alta, cards sem borda). Não editar `styles.css` nem `index.html` à mão, porque o render sobrescreve os dois.

## Passo 5 — Verificar (QA)

1. `.venv/Scripts/python.exe -I .claude/skills/criar-site/scripts/verificar.py sites/<slug>` precisa terminar sem ERRO.
2. Preview: `preview_start` com o nome `sites` (de `.claude/launch.json`, que serve a pasta `sites/` na porta 8800) e abrir `http://localhost:8800/<slug>/`.
3. Conferir no navegador:
   - **Celular** (`resize_window` com preset mobile) e **desktop**.
   - Rolar a página inteira: as seções aparecem, as animações rodam e nada fica invisível.
   - O botão do WhatsApp abre `wa.me/55…` com a mensagem certa.
   - O mapa mostra o lugar certo.
   - Não há erro no console (`read_console_messages`).
4. Corrigir o que falhar sem relatar. Voltar o viewport para desktop no fim e deixar o preview aberto em `http://localhost:8800/<slug>/`.

## Passo 6 — Entrega local (fim da skill)

A resposta final é **só isto**, sem mais texto:

```
**<Empresa>** — http://localhost:8800/<slug>/
Pendências: <itens curtos separados por " · ">
```

- A linha de pendências só aparece se houver algo que o Rafael precise confirmar: WhatsApp não confirmado, fotos de clientes usadas, seção cortada por falta de dado.
- **Nada vai para o GitHub nem para a Vercel** nesta etapa. Se o Rafael pedir ajuste, ajustar e responder de novo só com o link.

## Passo 7 — Publicar (só quando o Rafael pedir "publicar")

```
.venv/Scripts/python.exe -I .claude/skills/criar-site/scripts/publicar.py sites/<slug> --mensagem "Cria o site da <Empresa>"
```

O script cria o repo **privado** `<slug>` no GitHub, cria/atualiza o projeto `<slug>` na conta Vercel, faz o deploy de produção e registra a URL pública (`<slug>.vercel.app`, ou a variação que a Vercel atribuir se o nome estiver ocupado) em `sites/_controle.md`.

- O site usa `vercel.json` (cabeçalhos e noindex) e `.vercelignore` (não publica `site.json`), ambos gerados pelo render.
- O link da entrega é sempre o **alias de produção** `*.vercel.app`, nunca a URL única do deploy (essa fica protegida por login da Vercel).
- `vercel` sem login → abrir `vercel.cmd login` numa aba do terminal do Rafael (`run_in_terminal`) e pedir que ele autorize no navegador. Não tentar logar por ele.
- Instalar ferramentas globais (`npm -g`) sempre pelo terminal do Rafael, com `npm.cmd`. Instalação feita pelo Bash da sessão pode ficar isolada e não chegar ao Windows dele (aconteceu em 26/11/2026).

Depois, abrir a URL publicada no navegador e confirmar que carrega.

## Passo 8 — Entregar o link publicado

Mesmo modo silencioso. Responder só com:

1. **Link** `*.vercel.app` em destaque.
2. **Mensagem pronta para o WhatsApp do cliente**, curta e no tom da empresa. Exemplo para tom familiar:
   > Oi, <nome>! Aqui é o Rafael, falamos por telefone. Montei uma prévia do site da <Empresa> pra você ver como fica: <link>. Dá uma olhada no celular e me conta o que achou!

## Depois da venda

Quando o Rafael disser que fechou:

1. Mudar `demo: false` no `site.json`.
2. Rodar render e depois publicar.
3. Trocar o status no `_controle.md` para `vendido`.
4. Lembrar o Rafael de pedir ao cliente autorização das fotos e, se ele quiser, um domínio próprio.

## Regras fixas

- Uma empresa por vez, lendo páginas públicas como um usuário. Nada de raspagem em massa.
- Dados da empresa são públicos e comerciais. Não coletar dados pessoais de clientes além do primeiro nome + inicial nas avaliações.
- Não commitar `lista-imagens.txt` nem material bruto (o `.gitignore` do site já cobre isso).
- Este workspace é do Rafael (projeto Vendas Sites). Não misturar com Cronon nem com FreelancersBrasil.
