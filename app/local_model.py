"""Optional local-model adapter.

The safety-critical core of Survival AI does not require a language model.
This module provides a future integration point for Ollama, llama.cpp, or
another local runtime. Generated prose should always be grounded in the
deterministic engine and offline knowledge base.
"""

from dataclasses import dataclass


@dataclass
class LocalModelConfig:
    provider: str = "disabled"
    model: str | None = None


class LocalModelAdapter:
    def __init__(self, config: LocalModelConfig | None = None) -> None:
        self.config = config or LocalModelConfig()

    @property
    def enabled(self) -> bool:
        return self.config.provider != "disabled" and bool(self.config.model)

    def generate(self, prompt: str) -> str:
        if not self.enabled:
            raise RuntimeError("No local language model is configured.")
        raise NotImplementedError(
            "Connect this adapter to Ollama, llama.cpp, or another local model runtime."
        )
