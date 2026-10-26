"""Adaptador Windows para o LLM Council, sem alterar modelos ou contornar permissões."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def executable(provider: str) -> str:
    if provider == "claude" and os.name == "nt":
        # O launcher npm chama este binário nativo; evita shell e política .ps1.
        binary = (Path(os.environ.get("APPDATA", "")) / "npm" / "node_modules"
                  / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe")
        if binary.is_file():
            return str(binary)
    binary = shutil.which(provider)
    if not binary:
        raise FileNotFoundError(f"CLI não encontrada: {provider}")
    return binary


def run(provider: str, prompt: str, timeout: int) -> str:
    binary = executable(provider)
    if provider == "codex":
        with tempfile.TemporaryDirectory(prefix="council-codex-") as directory:
            output = Path(directory) / "response.md"
            command = [binary, "exec", "--skip-git-repo-check", "--ephemeral",
                       "--sandbox", "read-only", "--output-last-message", str(output), "-"]
            result = subprocess.run(command, input=prompt, text=True, encoding="utf-8",
                                    errors="replace", capture_output=True, timeout=timeout)
            if result.returncode:
                raise RuntimeError(f"Codex terminou com código {result.returncode}; verifique login e disponibilidade do modelo no cliente")
            if not output.is_file():
                raise RuntimeError("Codex não produziu a resposta final")
            return output.read_text(encoding="utf-8").strip()
    command = [binary, "-p", "--output-format", "text", "--max-turns", "1",
               "--no-session-persistence", "--tools", "", "--disable-slash-commands"]
    result = subprocess.run(command, input=prompt, text=True, encoding="utf-8",
                            errors="replace", capture_output=True, timeout=timeout)
    if result.returncode:
        if "credit balance is too low" in (result.stdout + result.stderr).lower():
            raise RuntimeError("Claude autenticado, mas sem saldo disponível (Credit balance is too low)")
        raise RuntimeError(f"Claude terminou com código {result.returncode}; verifique login e disponibilidade do modelo no cliente")
    if not result.stdout.strip():
        raise RuntimeError("Claude não produziu resposta")
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=["codex", "claude"])
    parser.add_argument("prompt", nargs="?", help="Se ausente, lê stdin")
    parser.add_argument("--timeout", type=int, default=150)
    parser.add_argument("--check", action="store_true", help="Verifica apenas o executável, sem API")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        if args.check:
            print(executable(args.provider))
            return
        prompt = args.prompt if args.prompt is not None else sys.stdin.read()
        if not prompt.strip():
            parser.error("Prompt vazio")
        print(run(args.provider, prompt, args.timeout))
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"{type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    main()
