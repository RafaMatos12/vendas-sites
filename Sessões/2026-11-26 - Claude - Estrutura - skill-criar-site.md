---
tipo: sessão
escopo: projeto
projeto: Vendas Sites
status: concluída
criado: 2026-11-26
atualizado: 2026-11-26
---

# 2026-11-26 — Claude — Estrutura — skill criar-site

## Data

2026-11-26

## Contexto

O Rafael quer levantar caixa vendendo sites de apresentação para estabelecimentos de Videira e região, por cold call. O pedido foi uma skill completa em que o papel dele se resume a dizer qual é a empresa. A skill coleta dados no Google Maps/Meu Negócio, analisa o Instagram (tom de voz), busca estrutura no Pinterest, monta o site (apresentação, o que vendem, localização, botão de WhatsApp), publica no GitHub e num serviço gratuito e devolve o link. No meio da sessão ele acrescentou que o site deve ser dinâmico, com efeitos que tragam experiência.

## Decisões tomadas

| Decisão | Porquê | Descartado |
|---|---|---|
| Workspace próprio `Documents\VendasSites`, com a skill em `.claude/skills/criar-site` | Regra do LimitLess: cada coisa mora em um lugar só; o vault guarda só o resumo | Skill global em `~/.claude/skills`, que misturaria com as skills da Cronon e do FB |
| Coleta pelo navegador do app, uma empresa por vez | Dispensa chave de API e conta no Google Cloud, e a escala é baixa | Google Places API: dado mais estável, mas exige projeto no GCP e chave |
| Deploy na **Netlify** | O plano grátis permite uso comercial | Vercel Hobby (proíbe uso comercial); Cloudflare Pages (equivalente, ficou como alternativa) |
| Conta Netlify com **e-mail diferente** do principal | Pedido do Rafael | — |
| **Um checkpoint** antes de publicar (preview + resumo da análise) | Evita publicar foto, texto ou WhatsApp errado sem revisão | Fluxo 100% automático |
| Repo **privado** por site; site demo com `noindex` até a venda | Dados e fotos de prospect não ficam públicos nem no Google antes do aceite | Repo público / GitHub Pages |
| Pinterest só como **inspiração de estrutura** | Copiar o design ou as imagens de um site específico é risco de direito autoral | Cópia 1:1 |
| Fotos: primeiro as do proprietário, depois o Instagram, por último as de clientes (avisando); nunca avatares de quem avaliou | Direitos de imagem e dado pessoal | — |
| HTML/CSS/JS estático, gerado por `render.py` a partir do `site.json`; ajustes por site em `custom.css` | Rápido, sem build, sem dependência; a base é consistente e o layout varia por site | Framework (Astro/Next): peso e manutenção sem ganho para one-page |
| Efeitos em 3 intensidades (`sutil`, `medio`, `marcante`), escolhidas pelo tom | Atende ao pedido de site dinâmico sem exagerar em marcas sérias/premium; respeita "reduzir movimento" | Mesmo nível de efeito para todos |
| Python do workspace em `.venv` com Pillow | Os scripts rodam com `python -I`, que ignora pacotes do usuário | Instalar com `--user` (não funciona com `-I`) |

## Testes feitos

- Site de exemplo com imagens fictícias: render e verificação sem erros (0,33 MB). Conferido no navegador em desktop e celular, sem erro no console, sem rolagem lateral e com o link do WhatsApp correto.
- Google Maps com uma padaria real de Videira: dados, nota, avaliações e fotos lidos; download e otimização de uma foto funcionando. Sem login, o Maps mostra uma "visualização limitada" (~3 avaliações).
- **Não testados:** `publicar.py` (falta a conta Netlify); Instagram e Pinterest num caso real (pedem login).

## Arquivos alterados

- `Documents\VendasSites\` (novo): `README.md`, `.gitignore`, `.claude/launch.json`, `.claude/skills/criar-site/` (SKILL.md, references, template, scripts), `sites/_controle.md`. Nada commitado.
- LimitLess: `02 - Projetos/StartUps/Vendas Sites.md` (nova) e `02 - Projetos/00 - Projetos.md` (entrada no índice).

## Próximos passos

| # | Ação | Dono |
|---|---|---|
| 1 | Criar a conta Netlify com o e-mail separado e rodar `netlify login` | Rafael |
| 2 | Primeiro site real: `/criar-site <Empresa>, Videira`, com login no Instagram/Pinterest no painel do navegador | Rafael + Claude |
| 3 | Validar `publicar.py` no primeiro deploy | Claude |
| 4 | Definir preço do site e roteiro da ligação | Rafael |
| 5 | Confirmar o critério de encerramento proposto na nota do vault | Rafael |
| 6 | Commit inicial do workspace (só com OK) | Claude |
| 7 | Decidir se o VendasSites entra na tabela de workspaces e de sessões das Regras Operacionais | Rafael |

## Atualização no mesmo dia — deploy trocado para a Vercel

O Rafael já tem um projeto de sites rodando na Vercel e preferiu concentrar tudo lá.

| Decisão | Porquê | Risco aceito |
|---|---|---|
| Deploy na **Vercel**, na conta que ele já usa, substituindo a Netlify | Um painel só para todos os sites | O plano Hobby (grátis) é só para uso não comercial; site vendido a cliente fica fora dos termos até migrar para o Pro (~US$ 20/mês) |

O que mudou na skill:
- `publicar.py` agora usa `vercel deploy --prod --project <slug> --create-if-missing` e devolve o alias público `*.vercel.app`, não a URL única do deploy, que é protegida.
- `render.py` gera `vercel.json` (cabeçalhos e noindex) e `.vercelignore` (não publica `site.json`) no lugar do `_headers`.
- SKILL.md e README foram atualizados.
- A Vercel CLI 67.0.0 foi instalada. A Netlify CLI continua instalada, mas sem uso.

Testado: render com `vercel.json` sem erros e o parser de URL do `publicar.py`. **Não testado:** o deploy real, porque a CLI está sem login. O passo 1 de "Próximos passos" agora é `vercel login`, e a conta Netlify deixou de ser necessária.

## Notas relacionadas

- LimitLess: `02 - Projetos/StartUps/Vendas Sites.md`
