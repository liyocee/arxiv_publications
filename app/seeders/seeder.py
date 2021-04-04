from abc import ABC, abstractmethod


class DatabaseSeeder(ABC):
    """
    Base class from which all the seeders should drive from
    """

    @abstractmethod
    def seed(self) -> None:
        raise NotImplementedError
