"""Checa um site antes do checkpoint: campos obrigatórios, WhatsApp, imagens, peso.

Uso:
    python -I verificar.py <pasta-do-site>

Sai com código 1 se houver erro bloqueante. Avisos não bloqueiam.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

OBRIGATORIOS = ["nome", "segmento", "cidade", "endereco"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")



def main(pasta: Path) -> int:
    erros, avisos = [], []
    d = json.loads((pasta / "site.json").read_text(encoding="utf-8"))
    e = d.get("empresa", {})
    for campo in OBRIGATORIOS:
        if not e.get(campo):
            erros.append(f"empresa.{campo} vazio")

    wa = re.sub(r"\D", "", e.get("whatsapp", ""))
    if not wa:
        erros.append("sem WhatsApp — o botão principal do site depende dele")
    else:
        local = wa[2:] if wa.startswith("55") else wa
        if len(local) == 10:
            avisos.append(f"WhatsApp {e['whatsapp']} parece FIXO (8 dígitos). Confirme se tem WhatsApp Business nesse número.")
        elif len(local) != 11:
            erros.append(f"WhatsApp com formato estranho: {e['whatsapp']}")

    if not d.get("hero", {}).get("imagem") and d.get("hero", {}).get("variante") != "centralizado":
        avisos.append("hero sem imagem — use variante 'centralizado' ou adicione uma foto")
    if not d.get("oferta", {}).get("itens"):
        avisos.append("sem itens em 'oferta' (o que vendem/fazem)")
    if not d.get("avaliacoes", {}).get("destaques"):
        avisos.append("sem avaliações em destaque")
    if d.get("demo", True) is False:
        avisos.append("demo=false: o site ficará INDEXÁVEL no Google (só depois da venda)")

    html = (pasta / "index.html").read_text(encoding="utf-8") if (pasta / "index.html").exists() else ""
    if not html:
        erros.append("index.html não existe — rode o render.py")
    for ref in sorted(set(re.findall(r'(?:src|href)="(img/[^"]+)"', html))):
        if not (pasta / ref).exists():
            erros.append(f"imagem referenciada não existe: {ref}")
    for txt in ("lorem ipsum", "TODO", "XXXX", "{{", "EXEMPLO"):
        if (txt in html) if txt.isupper() else (txt in html.lower()):
            erros.append(f"texto provisório no HTML: {txt!r}")

    peso = sum(p.stat().st_size for p in pasta.rglob("*") if p.is_file() and ".git" not in p.parts) / 1024 / 1024
    (avisos if peso > 5 else []).append(f"site pesado: {peso:.1f} MB (ideal < 5 MB)")

    for a in avisos:
        print(f"AVISO  {a}")
    for er in erros:
        print(f"ERRO   {er}")
    print(f"\nPeso total: {peso:.2f} MB · {len(erros)} erro(s), {len(avisos)} aviso(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.exit(main(Path(sys.argv[1]).resolve()))
