# Referência de estrutura no Pinterest

Objetivo: escolher **como o site se organiza**, não copiar um site existente.

## Buscar

1. Abrir `https://br.pinterest.com/search/pins/?q=<termos>` no navegador embutido. Se pedir login, o Rafael entra no painel.
2. Termos, em inglês e português, do mais específico ao mais geral:
   - `<segmento> website design` (ex.: `bakery website design`, `barbershop landing page`)
   - `<segmento> landing page <tom>` (ex.: `modern`, `elegant`, `playful`, `rustic`)
   - `site <segmento> moderno`
3. Ver 15–25 pins e escolher **2–3** que combinem com o tom e as fotos que a empresa tem. Uma referência linda que exige fotos profissionais que a empresa não tem é uma referência errada.

## Extrair de cada referência

| Aspecto | Vira no site |
|---|---|
| Composição do topo | `hero.variante`: `split` (texto + foto lado a lado), `imagem-cheia` (foto de fundo com texto em cima) ou `centralizado` (sem foto, tipografia forte) |
| Ordem das seções | ordem do conteúdo; seções sem dado simplesmente não entram |
| Ritmo de cores | seções alternando fundo claro e cor da marca → `custom.css` |
| Tipografia | caixa alta, serifada ou sem serifa, peso → `custom.css` ou `tema.fontes` |
| Cards | com foto, numerados, com borda ou sem → `oferta.itens[].imagem` e `custom.css` |
| Detalhes | formas, linhas, recortes, sobreposição de fotos → `custom.css` |

## Regras

- **Inspiração, não cópia.** Não reproduzir logo, ilustrações, textos ou fotos de um pin, nem o layout idêntico de um site específico. Combinar ideias de 2–3 referências.
- Guardar os links escolhidos em `site.json → referencias` (não aparecem no site; servem de registro).
- O `custom.css` deve ficar pequeno (até ~80 linhas). Se precisar de muito mais, a referência não combina com o template e deve ser trocada.

## Exemplos de ajustes em custom.css

```css
/* Hero com fundo na cor da marca e texto claro (referência "bold") */
.hero{background:var(--cor-primaria);color:#fff}
.hero .hero-sub,.hero .sobretitulo{color:rgba(255,255,255,.85)}

/* Títulos em caixa alta com espaçamento (referência "editorial") */
h1,h2{text-transform:uppercase;letter-spacing:.04em}

/* Seção de oferta escura (ritmo de contraste) */
.oferta{background:var(--cor-texto);color:var(--cor-fundo)}
.oferta .card{background:color-mix(in srgb,var(--cor-fundo) 8%,transparent)}
.oferta .card-corpo p{color:color-mix(in srgb,var(--cor-fundo) 70%,transparent)}
```
