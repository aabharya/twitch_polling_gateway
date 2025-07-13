from django.contrib.auth.models import UserManager
from django.db import models


class UserObjectManager(UserManager):
    """
    Custom user manager for User
    """

    def get_queryset(self):
        """
        Return a new QuerySet object. Subclasses can override this method to
        customize the behavior of the Manager.
        """
        return UserQuerySetManager(model=self.model, using=self._db, hints=self._hints)


class UserQuerySetManager(models.QuerySet):
    """
    Custom queryset manager for User
    """

    pass
