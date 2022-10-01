from enum import Enum, unique

@unique
class Scope(Enum):
    _ignore_ = '_SCOPE_HIERARCHY'

    PACK = 'pack'
    SONG = 'song'
    # SSC_FILE = 'ssc_file'
    # SM_FILE = 'sm_file'
    # CHART = 'chart'
    # SSC_CHART = 'ssc_chart'
    # SM_CHART = 'sm_chart'

    _SCOPE_HIERARCHY: dict['Scope', list['Scope']] = {
        PACK: [SONG],
        # SONG: [CHART, SSC_FILE, SM_FILE],
        # SSC_FILE: [SSC_CHART],
        # SM_FILE: [SM_CHART],
        # CHART: [SSC_CHART, SM_CHART],
    }

    def __gt__(self, other: 'Scope') -> bool:
        if other == self:
            return False

        descendants = self._SCOPE_HIERARCHY.get(self, [])
        if other in descendants:
            return True
        
        return any(descendant > other for descendant in descendants)
        