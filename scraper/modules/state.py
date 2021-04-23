from abc import ABC, abstractmethod

class State(ABC):

    @abstractmethod
    def info(self) -> None:
        """Print information."""
    pass

    @abstractmethod
    def select(self) -> any:
        """Select file."""
    pass

    @abstractmethod
    def create_JSON(self, files:list) -> any:
        """Create JSON."""
    pass