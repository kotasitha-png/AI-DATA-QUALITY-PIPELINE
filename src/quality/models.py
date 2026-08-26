from dataclasses import dataclass
from typing import Optional


@dataclass
class RuleResult:
    """
    Represents the result of one data-quality rule.
    """

    rule_id: str
    rule_type: str
    column: str
    severity: str

    passed: bool

    failed_count: int
    total_count: int

    failure_percentage: float

    message: str

    condition_description: Optional[str] = None