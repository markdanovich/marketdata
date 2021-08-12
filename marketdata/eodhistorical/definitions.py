from enum import Enum


class EndPoint(Enum):
    EXCHANGES = "exchanges-list"
    LIST_OF_TICKERS = "exchange-symbol-list"
    EOD = "eod"
    FUNDAMENTALS = "fundamentals"
    BOND_FUNDAMENTALS = "bond-fundamentals"
    MACRO = "macro-indicator"


class Period(Enum):
    DAY = "d"
    WEEK = "w"
    MONTH = "m"
    QUARTER = "q"
    AMNUAL = "y"
