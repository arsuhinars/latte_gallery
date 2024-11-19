from abc import ABC, abstractmethod
from typing import Iterable

from latte_gallery.accounts.models import Account, Role


class BasePermission(ABC):
    @abstractmethod
    def check_permission(self, account: Account | None):
        pass


class Anonymous(BasePermission):
    def check_permission(self, account):
        return account is None


class Authenticated(BasePermission):
    def check_permission(self, account):
        return account is not None


class HasRole(BasePermission):
    def __init__(self, role: Role):
        self._role = role

    def check_permission(self, account):
        return account is not None and account.role == self._role


class HasAnyRole(BasePermission):
    def __init__(self, roles: Iterable[Role]):
        self._roles = set(roles)

    def check_permission(self, account):
        return account is not None and account.role in self._roles


class IsAdmin(HasAnyRole):
    def __init__(self):
        super().__init__([Role.ADMIN, Role.MAIN_ADMIN])
