"""Baixa e otimiza as imagens de um site (WebP, largura máxima 1600px).

Uso:
    python -I imagens.py <pasta-do-site> <lista.txt>

<lista.txt>: uma imagem por linha, no formato  nome-do-arquivo  URL-ou-caminho-local
    hero        https://lh3.googleusercontent.com/...=w1600
    galeria-1   C:\\Users\\...\\foto.jpg
Linhas vazias e começando com # são ignoradas.

Saída: <pasta-do-site>/img/<nome>.webp — referencie no site.json como "img/<nome>.webp".
Só aceita https e arquivos locais; o conteúdo baixado é validado como imagem pelo Pillow.
"""
from __future__ import annotations

import io
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


LARGURA_MAX = 1600
TAMANHO_MAX = 15 * 1024 * 1024
AGENTE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def ampliar_url_google(url: str) -> str:
    """Fotos do Google (googleusercontent) aceitam sufixo de tamanho: pede a versão grande."""
    if "googleusercontent.com" in url:
        return re.sub(r"=[swh]\d+[^/?#]*$", "", url) + f"=w{LARGURA_MAX}"
    return url


def ler(origem: str) -> bytes:
    if origem.startswith("https://"):
        req = urllib.request.Request(ampliar_url_google(origem), headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(req, timeout=30) as r:
            dados = r.read(TAMANHO_MAX + 1)
    elif origem.startswith("http://"):
        raise ValueError("só https")
    else:
        dados = Path(origem).read_bytes()
    if len(dados) > TAMANHO_MAX:
        raise ValueError("arquivo grande demais")
    return dados


def main(pasta: Path, lista: Path) -> None:
    destino = pasta / "img"
    destino.mkdir(parents=True, exist_ok=True)
    ok = falhas = 0
    for linha in lista.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        nome, origem = linha.split(maxsplit=1)
        nome = re.sub(r"[^a-z0-9-]", "-", nome.lower())
        try:
            img = Image.open(io.BytesIO(ler(origem.strip())))
            img = ImageOps.exif_transpose(img).convert("RGB")
            if img.width > LARGURA_MAX:
                img = img.resize((LARGURA_MAX, round(img.height * LARGURA_MAX / img.width)), Image.LANCZOS)
            saida = destino / f"{nome}.webp"
            img.save(saida, "WEBP", quality=80, method=6)
            print(f"ok   img/{nome}.webp  {img.width}x{img.height}  {saida.stat().st_size // 1024} KB")
            ok += 1
        except Exception as erro:  # noqa: BLE001 — relatar e seguir para a próxima
            print(f"FALHA {nome}: {erro}")
            falhas += 1
    print(f"\n{ok} imagem(ns) prontas, {falhas} falha(s).")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
