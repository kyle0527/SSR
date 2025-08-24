class ContractViolation(Exception):
    """Finding/Config breaks declared contract (schema/required fields)."""

class UsefulnessBelowThreshold(Exception):
    """Finding exists but deemed not useful enough to include."""

class StopSignal(Exception):
    """Raised when StopPolicy decides to halt or skip further processing."""