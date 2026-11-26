# Vendas Sites

Esteira para levantar caixa: **cold call** para estabelecimentos de Videira e região, oferecendo um site de apresentação. O site já fica pronto e no ar antes da ligação de fechamento.

## Como usar

Abrir o Claude Code nesta pasta e pedir:

```
/criar-site Nome da Empresa, Videira
```

A skill (`.claude/skills/criar-site/`) segue estes passos:

1. Coleta no Google Maps (dados, avaliações, fotos).
2. Analisa o Instagram (tom de voz e identidade visual).
3. Busca referência de estrutura no Pinterest.
4. Gera o site one-page com efeitos.
5. Verifica o site.
6. **Entrega só o link do localhost** (`http://localhost:8800/<slug>/`), sem narrar o processo, para economizar tokens.
7. Quando você disser **"publicar"**: sobe num repo privado no GitHub e na Vercel (`<slug>.vercel.app`).
8. Entrega o link público e uma mensagem pronta para mandar ao cliente.

## Estrutura

| Caminho | O quê |
|---|---|
| `.claude/skills/criar-site/SKILL.md` | O fluxo completo |
| `.claude/skills/criar-site/references/` | Regras de coleta, rubrica de tom, uso do Pinterest, exemplo de `site.json` |
| `.claude/skills/criar-site/template/` | `styles.css` e `main.js` base (efeitos, responsivo) |
| `.claude/skills/criar-site/scripts/` | `render.py`, `imagens.py`, `verificar.py`, `publicar.py` |
| `sites/<slug>/` | Cada site, que é um repositório próprio no GitHub (ignorado aqui) |
| `sites/_controle.md` | Empresa, link, repo, status (demo / vendido / recusado) |

## Setup (uma vez por máquina)

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install pillow
npm.cmd i -g vercel      # .cmd contorna o bloqueio de scripts .ps1 do PowerShell
vercel.cmd login
gh auth status
```

## Efeitos do site

Intensidade por site em `site.json → efeitos` (`sutil`, `medio` ou `marcante`). Os efeitos são:

- entrada animada do topo e revelação das seções ao rolar, em cascata;
- parallax na foto principal;
- contador animado da nota e do número de avaliações;
- faixa de diferenciais em movimento;
- inclinação 3D nos cards e zoom nas fotos;
- lightbox na galeria;
- menu mobile com transição circular;
- barra de progresso de leitura;
- topo que encolhe e se esconde ao rolar;
- botão do WhatsApp com pulso e balão.

Quem ativa "reduzir movimento" no celular recebe o site sem animações.
