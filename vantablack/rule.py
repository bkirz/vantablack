from dataclasses import dataclass
from typing import Any, Generic, Literal, Protocol, TypeVar

from vantablack.scope import Scope
from simfile.dir import SimfileDirectory, SimfilePack
from simfile.sm import SMChart, SMSimfile
from simfile.ssc import SSCChart, SSCSimfile
from simfile.types import Chart

T = TypeVar("T")
S = TypeVar("S", bound=Scope)


@dataclass
class RuleViolation(Generic[T]):
    message: str
    originating_rule: "Rule"
    target: T


class Rule(Protocol[T, S]):
    name: str
    scope: S

    def __init__(self, config: Any):
        pass

    def apply(self, target: T) -> list[RuleViolation[T]]:
        raise NotImplementedError


PackRule = Rule[SimfilePack, Literal[Scope.PACK]]
SongRule = Rule[SimfileDirectory, Literal[Scope.SONG]]