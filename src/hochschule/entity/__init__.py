"""Entity-Klassen für das Hochschule-Modell."""

from hochschule.entity.adresse import Adresse
from hochschule.entity.base import Base
from hochschule.entity.hochschule import Hochschule
from hochschule.entity.student import Student

__all__ = ["Adresse", "Base", "Hochschule", "Student"]
