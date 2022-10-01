from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

from simfile.dir import SimfilePack, SimfileDirectory
from simfile.sm import SMSimfile, SMChart
from simfile.ssc import SSCSimfile, SSCChart
from simfile.types import Chart

from scope import Scope


T = TypeVar('T')
S = TypeVar('S', bound=Scope)

@dataclass
class RuleViolation(Generic[T]):
    message: str
    originating_rule: 'Rule'
    target: T


class Rule(Protocol[T, S]):
    name: str
    scope: S

    def apply(self, target: T) -> list[RuleViolation[T]]:
        raise NotImplementedError
        


PackRule = Rule[SimfilePack, Scope.PACK]
SongRule = Rule[SimfileDirectory, Scope.SONG]

# SSCFileRule = Rule[SSCSimfile, Scope.SSC_FILE]
# SMFileRule = Rule[SMSimfile, Scope.SM_FILE]

# ChartRule = Rule[Chart, Scope.CHART]
# SSCChartRule = Rule[SSCChart, Scope.SSC_CHART]
# SChartRule = Rule[SMChart, Scope.SM_CHART]