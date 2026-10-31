from typing import Optional
from .base import BaseAgent


class NpmAgent(BaseAgent):
    name = "npm"
    description = "Runs read-only npm commands (--version, list, outdated, audit)."
    keywords = ["npm", "node package", "package.json"]
    allowed_prefixes = ["npm", "npx"]
    forbidden_patterns = ["install -g", "uninstall", "rm -rf", "publish"]

    def build_command(self, text: str) -> Optional[list[str]]:
        t = text.lower()

        if "version" in t:
            return ["npm", "--version"]
        if "outdated" in t:
            return ["npm", "outdated"]
        if "audit" in t:
            return ["npm", "audit"]
        if "list" in t or "packages" in t or "installed" in t:
            return ["npm", "list", "--depth=0"]

        return None
