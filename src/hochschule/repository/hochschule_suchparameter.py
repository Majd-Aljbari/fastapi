"""Filter für die Hochschulsuche."""

from dataclasses import dataclass

__all__ = ["HochschuleSuchparameter"]


@dataclass(frozen=True, slots=True, kw_only=True)
class HochschuleSuchparameter:
    """Suchparameter für die Hochschulsuche."""

    name: str | None = None
    """Teil des Namens der Hochschule als Suchparameter."""

    def is_empty(self) -> bool:
        """Prüft, ob kein Suchparameter gesetzt ist."""
        return self.name is None
