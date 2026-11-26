# Análise do Instagram — tom de voz e identidade visual

## Achar o perfil

1. Usar o @ que o Rafael passou ou o link que aparece no perfil do Google.
2. Se não tiver, buscar no Google: `"<nome da empresa>" <cidade> instagram`.
3. Confirmar que é o perfil certo: mesma cidade/endereço na bio, mesmo segmento, e fotos coerentes com as do Google.
4. Abrir `https://www.instagram.com/<usuario>/` no navegador embutido. Se pedir login, o Rafael entra no painel. Nunca digitar senha.

## O que ler (sem baixar nada além das fotos escolhidas)

| Item | Para quê |
|---|---|
| Bio, link e destaques | slogan, serviços, horário e WhatsApp (confirmar com o Google) |
| Últimas ~12 legendas | tom de voz, vocabulário, emojis, gírias locais |
| Grade de fotos | paleta dominante, estilo (claro/escuro, produto/pessoas), qualidade |
| Posts fixados | o que a empresa considera mais importante |

Para ler legendas, abrir 3–5 posts e usar `get_page_text`. Para fotos, abrir o post e ler o `src` da imagem com `read_page`/`find`, ou com `javascript_tool` apenas para inspecionar atributos. As URLs do CDN do Instagram expiram, então baixar logo com `imagens.py`.

## Classificar o tom (`tema.tom`)

| Tom | Sinais | Exemplos de segmento |
|---|---|---|
| `descontraido` | muitos emojis, gírias, memes, "galera", exclamações, cores vivas | lanchonete, açaí, hamburgueria, pet shop, loja jovem |
| `familiar` | "você", "nossa família", tradição, receitas, fotos do dono e da equipe | padaria, restaurante caseiro, mercado, confeitaria |
| `profissional` | linguagem objetiva, técnica, sem gíria, dados e serviços | clínica, contabilidade, oficina, autopeças, construção |
| `premium` | frases curtas, poucas emojis, palavras como "exclusivo", "experiência", fotos editoriais e escuras | estética, joalheria, vinhos, arquitetura, restaurante sofisticado |

Na dúvida entre dois tons, escolher o mais próximo de como **a empresa escreve**, não do segmento.

## Intensidade dos efeitos (`efeitos`)

| Valor | Quando |
|---|---|
| `sutil` | premium, profissional sério (clínica, advocacia) |
| `medio` | padrão para a maioria dos casos |
| `marcante` | descontraído, público jovem, marca com muita energia nos posts |

## Paleta e fontes

- Tirar a **cor primária** da logo ou da cor que mais se repete na grade. A secundária é um acento que combine com ela.
- Garantir contraste: texto escuro em fundo claro. Se a cor da marca for clara demais para botão ou texto, escurecer.
- Fontes: usar o padrão do tom (`render.py → TONS`) e só trocar se a marca tiver estilo muito próprio, sempre por uma fonte do Google Fonts.

## Saída desta etapa

Anotar (no raciocínio, e depois no `site.json`):

- `tema.tom`, `tema.cores` (se diferentes do padrão) e `efeitos`.
- 3–5 expressões reais da empresa para usar nos textos.
- Slogan, se houver.
- Fotos candidatas (URLs) com uma descrição curta de cada.
- `empresa.instagram`.
