"""Gera o site one-page de uma empresa a partir do site.json.

Uso:
    python -I render.py <pasta-do-site>

Lê <pasta-do-site>/site.json e escreve, na mesma pasta:
    index.html, styles.css (base, sempre atualizado), main.js,
    custom.css (só se não existir — é onde vão os ajustes do site),
    favicon.svg, robots.txt, _headers (noindex enquanto demo=true).
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote, quote_plus

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


TEMPLATE = Path(__file__).resolve().parent.parent / "template"

# Paletas e fontes padrão por tom de voz — o site.json pode sobrescrever.
TONS = {
    "descontraido": {
        "cores": {"primaria": "#E4572E", "secundaria": "#FFC914", "fundo": "#FFFBF5",
                  "superficie": "#FFFFFF", "texto": "#2B2118", "suave": "#6B5D52"},
        "fontes": {"titulo": "Baloo 2", "corpo": "Nunito"}, "raio": "20px",
    },
    "familiar": {
        "cores": {"primaria": "#8B4513", "secundaria": "#D9A441", "fundo": "#FBF7F0",
                  "superficie": "#FFFFFF", "texto": "#2E2418", "suave": "#6F6253"},
        "fontes": {"titulo": "Lora", "corpo": "Source Sans 3"}, "raio": "14px",
    },
    "profissional": {
        "cores": {"primaria": "#1F4E79", "secundaria": "#2E86AB", "fundo": "#F6F8FA",
                  "superficie": "#FFFFFF", "texto": "#1B2430", "suave": "#5A6675"},
        "fontes": {"titulo": "Montserrat", "corpo": "Inter"}, "raio": "10px",
    },
    "premium": {
        "cores": {"primaria": "#1C1C1C", "secundaria": "#B8975A", "fundo": "#F7F4EF",
                  "superficie": "#FFFFFF", "texto": "#1C1C1C", "suave": "#6B655C"},
        "fontes": {"titulo": "Playfair Display", "corpo": "Jost"}, "raio": "2px",
    },
}

ICONES = {
    "whatsapp": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm5.8 14.07c-.24.68-1.42 1.3-1.95 1.35-.5.05-.98.23-3.3-.69-2.79-1.1-4.56-3.96-4.7-4.14-.13-.18-1.12-1.49-1.12-2.85 0-1.35.71-2.02.96-2.3.25-.27.55-.34.73-.34h.52c.17 0 .4-.06.62.47.24.55.8 1.92.87 2.06.07.14.12.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.72 1.19 1.55 1.93 1.07.95 1.97 1.25 2.24 1.39.28.14.44.11.6-.07.16-.18.69-.8.87-1.08.18-.27.37-.23.62-.14.25.09 1.6.76 1.88.9.27.13.46.2.52.32.07.11.07.66-.17 1.34Z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>',
    "relogio": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 10.41V7h-2v6.41l4.29 4.3 1.42-1.42L13 12.41Z"/></svg>',
    "telefone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.01-.24c1.12.37 2.33.57 3.58.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.46.57 3.58a1 1 0 0 1-.25 1.01l-2.2 2.2Z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2Zm-.2 2A3.6 3.6 0 0 0 4 7.6v8.8A3.6 3.6 0 0 0 7.6 20h8.8a3.6 3.6 0 0 0 3.6-3.6V7.6A3.6 3.6 0 0 0 16.4 4H7.6Zm9.65 1.5a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z"/></svg>',
    "estrela": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="m12 17.27 6.18 3.73-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17Z"/></svg>',
}


def esc(valor) -> str:
    return html.escape(str(valor or ""), quote=True)


def slugify(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")


def so_digitos(texto: str) -> str:
    return re.sub(r"\D", "", texto or "")


def numero_whatsapp(bruto: str) -> str:
    """Normaliza para 55DDDNNNNNNNNN. Aceita com ou sem 55."""
    d = so_digitos(bruto)
    if not d:
        return ""
    if not d.startswith("55"):
        d = "55" + d
    if len(d) not in (12, 13):
        raise SystemExit(f"WhatsApp inválido: {bruto!r} -> {d} (esperado 55 + DDD + número)")
    return d


def link_whatsapp(numero: str, mensagem: str) -> str:
    return f"https://wa.me/{numero}?text={quote(mensagem)}"


def estrelas(n: float) -> str:
    cheias = int(round(n or 0))
    return "".join(
        f'<span class="estrela{"" if i < cheias else " vazia"}">{ICONES["estrela"]}</span>'
        for i in range(5)
    )


def tema(dados: dict) -> dict:
    t = dados.get("tema", {})
    base = TONS.get(t.get("tom", "profissional"), TONS["profissional"])
    return {
        "cores": {**base["cores"], **t.get("cores", {})},
        "fontes": {**base["fontes"], **t.get("fontes", {})},
        "raio": t.get("raio", base["raio"]),
        "variante_hero": dados.get("hero", {}).get("variante", "split"),
    }


def google_fonts(fontes: dict) -> str:
    familias = []
    for nome in dict.fromkeys([fontes["titulo"], fontes["corpo"]]):
        familias.append("family=" + quote_plus(nome) + ":wght@400;500;600;700")
    return "https://fonts.googleapis.com/css2?" + "&".join(familias) + "&display=swap"


def secao_hero(d, e, wa) -> str:
    h = d.get("hero", {})
    img = h.get("imagem", "")
    variante = h.get("variante", "split")
    nota = d.get("avaliacoes", {})
    selo = ""
    if nota.get("nota"):
        selo = (f'<p class="selo-nota">{estrelas(nota["nota"])}'
                f'{numero_contavel(nota["nota"], 1)}'
                f'<span>{numero_contavel(nota.get("total", ""))} avaliações no Google</span></p>')
    estilo_bg = f' style="--hero-img:url(\'{esc(img)}\')"' if img and variante == "imagem-cheia" else ""
    midia = (f'<div class="hero-midia"><img src="{esc(img)}" alt="{esc(h.get("alt", e["nome"]))}" '
             f'width="1200" height="900" fetchpriority="high"></div>') if img and variante == "split" else ""
    return f"""
<section class="hero hero--{esc(variante)}" id="inicio"{estilo_bg}>
  <div class="container hero-grid">
    <div class="hero-texto revelar">
      <p class="sobretitulo">{esc(e.get("segmento"))} · {esc(e.get("cidade"))}</p>
      <h1>{esc(h.get("titulo", e["nome"]))}</h1>
      <p class="hero-sub">{esc(h.get("subtitulo", e.get("slogan", "")))}</p>
      <div class="hero-acoes">
        <a class="botao botao--whats" href="{esc(wa)}" target="_blank" rel="noopener">{ICONES["whatsapp"]}<span>{esc(h.get("cta", "Chamar no WhatsApp"))}</span></a>
        <a class="botao botao--linha" href="#localizacao">{ICONES["pin"]}<span>Como chegar</span></a>
      </div>
      {selo}
    </div>
    {midia}
  </div>
</section>"""


def numero_contavel(valor, casas: int = 0) -> str:
    """Número que o main.js anima de 0 até o valor quando entra na tela."""
    texto = str(valor).replace(".", ",")
    return f'<strong data-contar="{esc(valor)}" data-casas="{casas}">{esc(texto)}</strong>'


def secao_faixa(d) -> str:
    """Faixa em movimento contínuo com diferenciais curtos (ex.: 'Entrega rápida')."""
    itens = d.get("faixa", [])
    if not itens:
        return ""
    linha = "".join(f"<span>{esc(x)}</span><i aria-hidden=\"true\">✦</i>" for x in itens)
    return f"""
<div class="faixa" aria-label="Diferenciais">
  <div class="faixa-trilho">{linha}{linha.replace('<span>', '<span aria-hidden="true">')}</div>
</div>"""


def secao_sobre(d) -> str:
    s = d.get("sobre")
    if not s:
        return ""
    destaques = "".join(f"<li>{ICONES['check']}<span>{esc(x)}</span></li>" for x in s.get("destaques", []))
    img = s.get("imagem")
    midia = f'<div class="sobre-midia revelar"><img src="{esc(img)}" alt="{esc(s.get("alt", ""))}" loading="lazy" width="900" height="1100"></div>' if img else ""
    paragrafos = "".join(f"<p>{esc(p)}</p>" for p in s.get("texto", []))
    return f"""
<section class="secao sobre" id="sobre">
  <div class="container sobre-grid{' sem-midia' if not img else ''}">
    {midia}
    <div class="revelar">
      <p class="sobretitulo">{esc(s.get("sobretitulo", "Quem somos"))}</p>
      <h2>{esc(s.get("titulo", ""))}</h2>
      {paragrafos}
      {f'<ul class="lista-check">{destaques}</ul>' if destaques else ''}
    </div>
  </div>
</section>"""


def secao_oferta(d) -> str:
    o = d.get("oferta")
    if not o or not o.get("itens"):
        return ""
    cards = []
    for i, item in enumerate(o["itens"], 1):
        img = item.get("imagem")
        topo = (f'<img src="{esc(img)}" alt="{esc(item["nome"])}" loading="lazy" width="600" height="450">'
                if img else f'<span class="card-num">{i:02d}</span>')
        cards.append(f"""<article class="card revelar">{topo}<div class="card-corpo"><h3>{esc(item["nome"])}</h3><p>{esc(item.get("descricao", ""))}</p></div></article>""")
    return f"""
<section class="secao oferta" id="oferta">
  <div class="container">
    <header class="cabecalho-secao revelar">
      <p class="sobretitulo">{esc(o.get("sobretitulo", "O que oferecemos"))}</p>
      <h2>{esc(o.get("titulo", ""))}</h2>
      {f'<p>{esc(o["descricao"])}</p>' if o.get("descricao") else ''}
    </header>
    <div class="grade-cards">{''.join(cards)}</div>
  </div>
</section>"""


def secao_galeria(d) -> str:
    fotos = d.get("galeria", [])
    if not fotos:
        return ""
    itens = "".join(
        f'<figure class="revelar"><img src="{esc(f["src"] if isinstance(f, dict) else f)}" '
        f'alt="{esc(f.get("alt", "") if isinstance(f, dict) else "")}" loading="lazy" width="800" height="800"></figure>'
        for f in fotos
    )
    return f"""
<section class="secao galeria" id="galeria">
  <div class="container">
    <header class="cabecalho-secao revelar"><p class="sobretitulo">Galeria</p><h2>{esc(d.get("galeria_titulo", "Um pouco do nosso dia a dia"))}</h2></header>
    <div class="grade-galeria">{itens}</div>
  </div>
</section>"""


def secao_avaliacoes(d) -> str:
    a = d.get("avaliacoes", {})
    lista = a.get("destaques", [])
    if not lista:
        return ""
    cards = "".join(
        f"""<figure class="depoimento revelar"><div class="estrelas">{estrelas(x.get("estrelas", 5))}</div>
<blockquote>“{esc(x["texto"])}”</blockquote><figcaption>{esc(x.get("autor", "Cliente"))}</figcaption></figure>"""
        for x in lista
    )
    resumo = ""
    if a.get("nota"):
        resumo = f'<p class="nota-grande">{numero_contavel(a["nota"], 1)} {estrelas(a["nota"])} <span>{numero_contavel(a.get("total", ""))} avaliações no Google</span></p>'
    return f"""
<section class="secao avaliacoes" id="avaliacoes">
  <div class="container">
    <header class="cabecalho-secao revelar"><p class="sobretitulo">Quem conhece, recomenda</p><h2>{esc(a.get("titulo", "O que nossos clientes dizem"))}</h2>{resumo}</header>
    <div class="grade-depoimentos">{cards}</div>
  </div>
</section>"""


def secao_local(d, e, wa) -> str:
    consulta = e.get("maps_consulta") or f'{e["nome"]}, {e.get("endereco", "")}'
    mapa = f"https://www.google.com/maps?q={quote_plus(consulta)}&output=embed"
    rota = e.get("maps_url") or f"https://www.google.com/maps/search/?api=1&query={quote_plus(consulta)}"
    horarios = "".join(f"<li><span>{esc(h['dias'])}</span><span>{esc(h['horas'])}</span></li>"
                       for h in e.get("horarios", []))
    tel = e.get("telefone")
    insta = e.get("instagram")
    return f"""
<section class="secao local" id="localizacao">
  <div class="container local-grid">
    <div class="revelar">
      <p class="sobretitulo">Venha nos visitar</p>
      <h2>{esc(d.get("local_titulo", "Onde estamos"))}</h2>
      <ul class="info-contato">
        <li>{ICONES["pin"]}<a href="{esc(rota)}" target="_blank" rel="noopener">{esc(e.get("endereco"))}</a></li>
        {f'<li>{ICONES["telefone"]}<a href="tel:+{so_digitos(tel) if so_digitos(tel).startswith("55") else "55" + so_digitos(tel)}">{esc(tel)}</a></li>' if tel else ''}
        {f'<li>{ICONES["instagram"]}<a href="https://instagram.com/{esc(insta.lstrip("@"))}" target="_blank" rel="noopener">@{esc(insta.lstrip("@"))}</a></li>' if insta else ''}
      </ul>
      {f'<div class="horarios"><h3>{ICONES["relogio"]} Horário de funcionamento</h3><ul>{horarios}</ul></div>' if horarios else ''}
      <a class="botao botao--whats" href="{esc(wa)}" target="_blank" rel="noopener">{ICONES["whatsapp"]}<span>Falar no WhatsApp</span></a>
    </div>
    <div class="mapa revelar"><iframe title="Mapa: {esc(e['nome'])}" src="{esc(mapa)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>"""


def schema_org(d, e) -> str:
    dados = {
        "@context": "https://schema.org",
        "@type": d.get("schema_tipo", "LocalBusiness"),
        "name": e["nome"],
        "description": d.get("seo", {}).get("descricao", e.get("slogan", "")),
        "address": {"@type": "PostalAddress", "streetAddress": e.get("endereco", ""),
                    "addressLocality": e.get("cidade", ""), "addressRegion": e.get("uf", ""),
                    "addressCountry": "BR"},
    }
    if e.get("telefone"):
        dados["telephone"] = e["telefone"]
    a = d.get("avaliacoes", {})
    if a.get("nota") and a.get("total"):
        dados["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": a["nota"],
                                    "reviewCount": a["total"]}
    return json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")


def render(pasta: Path) -> None:
    d = json.loads((pasta / "site.json").read_text(encoding="utf-8"))
    e = d["empresa"]
    t = tema(d)
    numero = numero_whatsapp(e.get("whatsapp", ""))
    mensagem = d.get("whatsapp_mensagem", f"Olá! Vim pelo site da {e['nome']} e gostaria de mais informações.")
    wa = link_whatsapp(numero, mensagem) if numero else "#localizacao"
    seo = d.get("seo", {})
    titulo = seo.get("titulo", f'{e["nome"]} · {e.get("segmento", "")} em {e.get("cidade", "")}')
    descricao = seo.get("descricao", e.get("slogan", ""))
    og = d.get("hero", {}).get("imagem", "")
    demo = d.get("demo", True)
    c = t["cores"]
    css_vars = (f':root{{--cor-primaria:{c["primaria"]};--cor-secundaria:{c["secundaria"]};'
                f'--cor-fundo:{c["fundo"]};--cor-superficie:{c["superficie"]};--cor-texto:{c["texto"]};'
                f'--cor-suave:{c["suave"]};--fonte-titulo:"{t["fontes"]["titulo"]}",Georgia,serif;'
                f'--fonte-corpo:"{t["fontes"]["corpo"]}",system-ui,sans-serif;--raio:{t["raio"]};}}')
    nav = [("Sobre", "#sobre", d.get("sobre")), (d.get("oferta", {}).get("menu", "O que fazemos"), "#oferta", d.get("oferta")),
           ("Avaliações", "#avaliacoes", d.get("avaliacoes", {}).get("destaques")),
           ("Localização", "#localizacao", True)]
    links_nav = "".join(f'<a href="{h}">{esc(n)}</a>' for n, h, ok in nav if ok)
    logo = d.get("logo")
    marca = (f'<img src="{esc(logo)}" alt="{esc(e["nome"])}" height="44">' if logo
             else f'<span>{esc(e["nome"])}</span>')

    pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descricao)}">
{'<meta name="robots" content="noindex, nofollow">' if demo else ''}
<meta name="theme-color" content="{esc(c["primaria"])}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descricao)}">
{f'<meta property="og:image" content="{esc(og)}">' if og else ''}
<meta property="og:locale" content="pt_BR">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{esc(google_fonts(t["fontes"]))}">
<link rel="stylesheet" href="styles.css">
<style>{css_vars}</style>
<link rel="stylesheet" href="custom.css">
<script type="application/ld+json">{schema_org(d, e)}</script>
</head>
<body class="tom-{esc(d.get("tema", {}).get("tom", "profissional"))}" data-efeitos="{esc(d.get("efeitos", "medio"))}">
<div class="progresso" aria-hidden="true"></div>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo" id="topo">
  <div class="container topo-barra">
    <a class="marca" href="#inicio">{marca}</a>
    <button class="menu-botao" aria-expanded="false" aria-controls="menu" aria-label="Abrir menu"><span></span><span></span><span></span></button>
    <nav id="menu" class="menu">{links_nav}<a class="botao botao--whats botao--pequeno" href="{esc(wa)}" target="_blank" rel="noopener">{ICONES["whatsapp"]}<span>WhatsApp</span></a></nav>
  </div>
</header>
<main id="conteudo">
{secao_hero(d, e, wa)}
{secao_faixa(d)}
{secao_sobre(d)}
{secao_oferta(d)}
{secao_avaliacoes(d)}
{secao_galeria(d)}
{secao_local(d, e, wa)}
</main>
<footer class="rodape">
  <div class="container rodape-grid">
    <p><strong>{esc(e["nome"])}</strong><br>{esc(e.get("endereco"))}</p>
    <p>© <span data-ano></span> {esc(e["nome"])}. Todos os direitos reservados.</p>
  </div>
</footer>
<a class="whats-flutuante" href="{esc(wa)}" target="_blank" rel="noopener" aria-label="Conversar no WhatsApp">{ICONES["whatsapp"]}<span class="whats-balao">{esc(d.get("whatsapp_balao", "Fale com a gente!"))}</span></a>
<div class="lightbox" hidden><button class="lightbox-fechar" aria-label="Fechar">×</button><img alt=""></div>
<script src="main.js" defer></script>
</body>
</html>
"""
    (pasta / "index.html").write_text(pagina, encoding="utf-8")
    shutil.copyfile(TEMPLATE / "styles.css", pasta / "styles.css")
    shutil.copyfile(TEMPLATE / "main.js", pasta / "main.js")
    if not (pasta / "custom.css").exists():
        (pasta / "custom.css").write_text(
            "/* Ajustes específicos deste site (layout da referência do Pinterest, detalhes do tom).\n"
            "   Este arquivo NÃO é sobrescrito pelo render.py. */\n", encoding="utf-8")
    inicial = esc((e["nome"].strip() or "?")[0].upper())
    (pasta / "favicon.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{esc(c["primaria"])}"/>'
        f'<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" font-family="Arial,sans-serif" font-size="36" font-weight="700" fill="#fff">{inicial}</text></svg>',
        encoding="utf-8")
    (pasta / "robots.txt").write_text("User-agent: *\n" + ("Disallow: /\n" if demo else "Allow: /\n"), encoding="utf-8")
    cabecalhos = "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
    if demo:
        cabecalhos += "  X-Robots-Tag: noindex, nofollow\n"
    (pasta / "_headers").write_text(cabecalhos, encoding="utf-8")
    print(f"OK: {pasta / 'index.html'}  (demo={demo}, whatsapp={'sim' if numero else 'NÃO'})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    render(Path(sys.argv[1]).resolve())
