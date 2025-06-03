from enum import Enum

class Type(str, Enum):
    UNDECIDED="Undecided"
    DECISION="Decision"
    UNCERTAINTY="Uncertainty"
    VALUE_METRIC="Value Metric"
    FACT="Fact"
    UTILITY="Utility"
    OTHER="Other"
    ACTION_ITEM="Action Item"

class Boundary(str, Enum):
    IN="in"
    ON="on"
    OUT="out"

class DatabaseConstants(int, Enum):
    MAX_SHORT_STRING_LENGTH=60
    MAX_LONG_STRING_LENGTH=600