from typing import Optional
from .base import BaseAgent


class DockerAgent(BaseAgent):
    name = "docker"
    description = "Runs read-only docker commands (ps, images, version, info)."
    keywords = ["docker", "container", "image"]
    allowed_prefixes = ["docker"]
    forbidden_patterns = ["rm", "rmi", "prune", "kill", "stop", "down", "system prune"]

    def build_command(self, text: str) -> Optional[list[str]]:
        t = text.lower()

        if "version" in t:
            return ["docker", "version"]
        if "info" in t:
            return ["docker", "info"]
        if "image" in t:
            return ["docker", "images"]
        if "container" in t or "ps" in t or "running" in t:
            return ["docker", "ps"]

        return None