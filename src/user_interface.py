from abc import ABC, abstractmethod

from src.project_types import UserData


class UserInterface(ABC):
    @abstractmethod
    def get_user_data(self) -> UserData: ...
