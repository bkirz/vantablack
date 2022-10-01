import rule
from typing import Optional

class Registry:
    '''A lookup table of all configured rule classes.'''

    def __init__(self, rule_classes: list[type[rule.Rule]]):
        self._rule_classes_by_name = {rc.name: rc for rc in rule_classes}

    def rule_class(self, name: str) -> Optional[type[rule.Rule]]:
        return self._rule_classes_by_name.get(name)