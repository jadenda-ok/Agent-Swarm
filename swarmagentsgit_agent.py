from typing import Optional
from .base import BaseAgent


class GitAgent(BaseAgent):
    name = "git"
    description = "Runs read-only git commands (status, log, diff, branch, remote)."
    keywords = ["git", "commit", "branch", "repo", "repository", "staged", "unstaged", "diff", "clone"]
    allowed_prefixes = ["git"]
    forbidden_patterns = ["--force", "push --mirror", "-f", "reset --hard"]

    def build_command(self, text: str) -> Optional[list[str]]:
        t = text.lower()

        if "current branch" in t or "which branch" in t or "what branch" in t:
            return ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        if "status" in t:
            return ["git", "status"]
        if "log" in t:
            return ["git", "log", "--oneline", "-20"]
        if "diff" in t:
            return ["git", "diff"]
        if "branch" in t:
            return ["git", "branch", "-a"]
        if "remote" in t:
            return ["git", "remote", "-v"]

        return None