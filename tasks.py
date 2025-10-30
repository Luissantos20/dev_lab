import subprocess
import sys


def sh(cmd):
    print(f"→ {cmd}")
    r = subprocess.run(cmd, shell=True)
    if r.returncode != 0:
        sys.exit(r.returncode)


def format():
    """Executa isort e black."""
    sh("isort .")
    sh("black .")


def lint():
    """Executa flake8."""
    sh("flake8 app")


def check():
    """Formata, organiza e valida código."""
    format()
    lint()


def run():
    """Inicia a API com Uvicorn."""
    sh("uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")


if __name__ == "__main__":
    cmds = {
        "format": format,
        "lint": lint,
        "check": check,
        "run": run,
    }
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print("Use: python tasks.py [format|lint|check|run]")
        sys.exit(1)
    cmds[sys.argv[1]]()
