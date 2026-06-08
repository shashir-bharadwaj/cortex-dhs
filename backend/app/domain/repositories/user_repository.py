from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.authenticated_user import AuthenticatedUser
from app.domain.entities.user import User


class UserRepository(ABC):
    """
    Repository contract for user persistence operations.
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """
        Persist a new user.
        """
        raise NotImplementedError

    @abstractmethod
    def by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve user by database id.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve user by public/business user id.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve user by email.
        """
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        hospital_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        role_id: Optional[int] = None,
    ) -> list[User]:
        """
        List users with optional filtering.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Update an existing user.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> None:
        """
        Soft delete/deactivate a user.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_auth_context_by_user_id(
        self,
        user_id: str,
    ) -> Optional[AuthenticatedUser]:
        """
        Load authenticated user with resolved permissions.
        """
        pass