"""Publica um site: repositório privado no GitHub + deploy de produção na Netlify.

Uso (SÓ depois do OK do Rafael no checkpoint):
    python -I publicar.py <pasta-do-site> [--mensagem "texto do commit"]

Primeira vez: git init, commit, `gh repo create <slug> --private --push`,
`netlify deploy --prod --site-name <slug>` (cria o site e liga a pasta).
Vezes seguintes: commit + push + `netlify deploy --prod` no site já ligado.
Imprime a URL final e atualiza sites/_controle.md.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

GITIGNORE = ".netlify/\nlista-imagens.txt\nbriefing.md\n"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")



def rodar(cmd: list[str], pasta: Path, checar: bool = True) -> str:
    exe = shutil.which(cmd[0]) or cmd[0]
    r = subprocess.run([exe, *cmd[1:]], cwd=pasta, capture_output=True, text=True, encoding="utf-8")
    if checar and r.returncode != 0:
        raise SystemExit(f"Falhou: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()


def git(pasta: Path, mensagem: str) -> str:
    if not (pasta / ".git").exists():
        rodar(["git", "init", "-b", "main"], pasta)
    gi = pasta / ".gitignore"
    if not gi.exists():
        gi.write_text(GITIGNORE, encoding="utf-8")
    rodar(["git", "add", "-A"], pasta)
    if rodar(["git", "status", "--porcelain"], pasta):
        rodar(["git", "commit", "-m", mensagem], pasta)
    slug = pasta.name
    remoto = rodar(["git", "remote"], pasta, checar=False)
    if "origin" not in remoto.split():
        rodar(["gh", "repo", "create", slug, "--private", "--source", ".", "--push"], pasta)
    else:
        rodar(["git", "push", "-u", "origin", "main"], pasta)
    return rodar(["gh", "repo", "view", "--json", "url", "-q", ".url"], pasta)


def netlify(pasta: Path, mensagem: str) -> str:
    base = ["netlify", "deploy", "--prod", "--dir", ".", "--no-build", "--json", "--message", mensagem]
    ligado = (pasta / ".netlify" / "state.json").exists()
    cmd = base if ligado else [*base, "--site-name", pasta.name]
    saida = rodar(cmd, pasta)
    inicio = saida.find("{")
    dados = json.loads(saida[inicio:]) if inicio >= 0 else {}
    return dados.get("url") or dados.get("deploy_url") or saida


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
    repo = git(pasta, mensagem)
    url = netlify(pasta, mensagem)
    registrar(pasta, repo, url)
    print(f"\nREPO {repo}\nSITE {url}")


if __name__ == "__main__":
    main()
