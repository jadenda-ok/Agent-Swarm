from typing import Optional
from .base import BaseAgent


class KubectlAgent(BaseAgent):
    name = "kubectl"
    description = "Runs read-only kubectl commands (get pods/nodes/svc, config current-context)."
    keywords = ["kubectl", "kube", "kubernetes", "pod", "pods", "node", "namespace", "context"]
    allowed_prefixes = ["kubectl"]
    forbidden_patterns = ["delete", "drain", "cordon", "apply", "edit", "scale", "exec"]

    def build_command(self, text: str) -> Optional[list[str]]:
        t = text.lower()

        if "context" in t:
            return ["kubectl", "config", "current-context"]
        if "namespace" in t:
            return ["kubectl", "get", "namespaces"]
        if "node" in t:
            return ["kubectl", "get", "nodes"]
        if "svc" in t or "service" in t:
            return ["kubectl", "get", "svc"]
        if "pod" in t:
            return ["kubectl", "get", "pods"]

        return None