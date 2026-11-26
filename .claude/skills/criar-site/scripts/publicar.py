"""Publica um site: repositório privado no GitHub + deploy de produção na Vercel.

Uso (SÓ depois do OK do Rafael no checkpoint):
    python -I publicar.py <pasta-do-site> [--mensagem "texto do commit"]

Primeira vez: git init, commit, `gh repo create <slug> --private --push` e
`vercel deploy --prod --project <slug> --create-if-missing` (cria o projeto na conta Vercel).
Vezes seguintes: commit + push + novo deploy de produção no mesmo projeto.
Imprime a URL pública (<slug>.vercel.app ou a variação que a Vercel atribuir)
e atualiza sites/_controle.md.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

GITIGNORE = ".vercel/\nlista-imagens.txt\nbriefing.md\n"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def rodar(cmd: list[str], pasta: Path, checar: bool = True) -> str:
    exe = shutil.which(cmd[0]) or cmd[0]
    r = subprocess.run([exe, *cmd[1:]], cwd=pasta, capture_output=True, text=True, encoding="utf-8")
    if checar and r.returncode != 0:
        raise SystemExit(f"Falhou: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return (r.stdout + "\n" + r.stderr).strip()


def git(pasta: Path, mensagem: str) -> str:
    if not (pasta / ".git").exists():
        rodar(["git", "init", "-b", "main"], pasta)
    gi = pasta / ".gitignore"
    if not gi.exists():
        gi.write_text(GITIGNORE, encoding="utf-8")
    rodar(["git", "add", "-A"], pasta)
    if rodar(["git", "status", "--porcelain"], pasta):
        rodar(["git", "commit", "-m", mensagem], pasta)
    remoto = rodar(["git", "remote"], pasta, checar=False)
    if "origin" not in remoto.split():
        rodar(["gh", "repo", "create", pasta.name, "--private", "--source", ".", "--push"], pasta)
    else:
        rodar(["git", "push", "-u", "origin", "main"], pasta)
    return rodar(["gh", "repo", "view", "--json", "url", "-q", ".url"], pasta).splitlines()[0]


def hosts_vercel(texto: str) -> list[str]:
    return sorted(set(re.findall(r"[a-z0-9][a-z0-9-]*\.vercel\.app", texto.lower())), key=len)


def vercel(pasta: Path) -> str:
    """Faz o deploy de produção e devolve a URL pública (o alias de produção)."""
    slug = pasta.name
    saida = rodar(["vercel", "deploy", ".", "--prod", "--yes", "--project", slug,
                   "--create-if-missing", "--json"], pasta)
    hosts = hosts_vercel(saida)
    # O deploy em si tem uma URL única (protegida); o público é o alias de produção.
    if hosts:
        detalhes = rodar(["vercel", "inspect", hosts[-1], "--json"], pasta, checar=False)
        hosts = hosts_vercel(saida + "\n" + detalhes)
    if f"{slug}.vercel.app" in hosts:
        return f"https://{slug}.vercel.app"
    aliases = [h for h in hosts if h.startswith(slug)]
    if aliases:
        return f"https://{aliases[0]}"
    raise SystemExit(f"Deploy feito, mas não achei a URL pública na saída:\n{saida}")


def registrar(pasta: Path, repo: str, url: str) -> None:
    controle = pasta.parent / "_controle.md"
    nome = json.loads((pasta / "site.json").read_text(encoding="utf-8"))["empresa"]["nome"]
    linhas = controle.read_text(encoding="utf-8").splitlines() if controle.exists() else []
    linhas = [l for l in linhas if f"`{pasta.name}`" not in l]
    linhas.append(f"| {date.today():%Y-%m-%d} | {nome} | `{pasta.name}` | {url} | {repo} | demo |")
    controle.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    pasta = Path(args[0]).resolve()
    mensagem = args[args.index("--mensagem") + 1] if "--mensagem" in args else "Publica o site"
    if not (pasta / "index.html").exists():
        raise SystemExit("index.html não encontrado — rode render.py antes.")
    if "Logged out" in rodar(["vercel", "whoami"], pasta, checar=False):
        raise SystemExit("Vercel CLI sem login: peça ao Rafael para rodar `vercel login`.")
    repo = git(pasta, mensagem)
    url = vercel(pasta)
    registrar(pasta, repo, url)
    print(f"\nREPO {repo}\nSITE {url}")


if __name__ == "__main__":
    main()
