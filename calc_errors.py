class CalcError(Exception):
    """Base error for invalid expressions,math domains,or overflow."""
class CalcSyntaxError(CalcError):
    """Raised when tokens or syntax structure are invalid."""

class CalcDomainError(CalcError):
    """Raised on invalid argument counts,names,ranges,or math domains."""

class CalcOverflowError(CalcError):
    """Raised when a calculation overflows numeric limits."""