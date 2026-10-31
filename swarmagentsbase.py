"""Base agent: every robot inherits from here."""
from __future__ import annotations

import subprocess
from typing import Optional


GLOBAL_DENYLIST = [
    "rm -rf",
    "rm -fr",
    "mkfs",
    "dd if=",
    "sudo rm",
    "chmod -R 777 /",
    "shutdown",
    "reboot",
    "> /dev/sd",
    ":(){",
]


class BaseAgent:
    name: str = "base"
    description: str = ""
    keywords: list[str] = []
    allowed_prefixes: list[str] = []
    forbidden_patterns: list[str] = []

    # ---------- routing ----------
    def can_handle(self, text: str) -> bool:
        t = text.lower()
        return any(k in t for k in self.keywords)

    # ---------- command construction ----------
    def build_command(self, text: str) -> Optional[list[str]]:
        """Turn a natural-language request into an argv list. Return None if unsure."""
        raise NotImplementedError

    # ---------- safety ----------
    def is_safe(self, cmd: list[str]) -> tuple[bool, str]:
        if not cmd:
            return False, "empty command"

        if self.allowed_prefixes and cmd[0] not in self.allowed_prefixes:
            return False, f"command must start with one of {self.allowed_prefixes}"

        joined = " ".join(cmd)
        for pat in GLOBAL_DENYLIST + self.forbidden_patterns:
            if pat in joined:
                return False, f"forbidden pattern: {pat}"

        return True, "ok"

    # ---------- execution ----------
    def run_command(self, cmd: list[str], dry_run: bool = False) -> dict:
        if dry_run:
            return {"ok": True, "agent": self.name, "command": cmd, "dry_run": True}
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {
                "ok": res.returncode == 0,
                "agent": self.name,
                "command": cmd,
                "returncode": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "agent": self.name, "command": cmd, "error": "timeout after 60s"}
        except FileNotFoundError:
            return {"ok": False, "agent": self.name, "command": cmd,
                    "error": f"'{cmd[0]}' is not installed"}

    def execute(self, text: str, dry_run: bool = False,
                command_override: Optional[list[str]] = None) -> dict:
        cmd = command_override if command_override is not None else self.build_command(text)
        if not cmd:
            return {
                "ok": False,
                "agent": self.name,
                "error": (
                    "I couldn't turn that into a safe command. "
                    "Try rephrasing, use --ai, or use the '!' prefix for a literal command."
                ),
            }
        safe, reason = self.is_safe(cmd)
        if not safe:
            return {"ok": False, "agent": self.name, "command": cmd, "error": f"unsafe: {reason}"}
        return self.run_command(cmd, dry_run=dry_run)