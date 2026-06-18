import signal
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> int:
    processos = [
        subprocess.Popen([sys.executable, "backend.py"], cwd=ROOT),
        subprocess.Popen([sys.executable, "frontend.py"], cwd=ROOT),
    ]

    print("Care on Live em execucao")
    print("Site: http://127.0.0.1:3000")
    print("API:  http://127.0.0.1:8080")
    print("Docs: http://127.0.0.1:8080/docs")
    print("Pressione Ctrl+C para parar.")

    def encerrar(_sinal=None, _frame=None):
        for processo in processos:
            if processo.poll() is None:
                processo.terminate()
        for processo in processos:
            try:
                processo.wait(timeout=5)
            except subprocess.TimeoutExpired:
                processo.kill()

    signal.signal(signal.SIGINT, encerrar)
    signal.signal(signal.SIGTERM, encerrar)

    try:
        while any(processo.poll() is None for processo in processos):
            for processo in processos:
                processo.wait(timeout=1)
    except (KeyboardInterrupt, subprocess.TimeoutExpired):
        encerrar()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
