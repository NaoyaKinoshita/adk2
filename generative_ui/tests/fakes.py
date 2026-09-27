from dataclasses import dataclass, field
from typing import Any


@dataclass
class FakeTool:
    name: str


@dataclass
class FakeToolContext:
    state: dict[str, Any] = field(default_factory=dict)
