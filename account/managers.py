from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, first_name=None, last_name=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone number')

        user = self.model(
            phone_number=self.normalize_email(phone_number), first_name=first_name, last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, first_name=None, last_name=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            first_name=first_name, 
            last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
