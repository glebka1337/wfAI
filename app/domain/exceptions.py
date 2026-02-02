class DomainError(Exception):
    """Base exception for domain layer."""
    pass

class PersonaAlreadyExists(DomainError):
    pass

class PersoneNotFound(DomainError):
    pass

class SessionNotFound(DomainError):
    pass