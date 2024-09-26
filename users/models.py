from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError('Users must have an email address')
        if password is None:
            raise ValueError('Users must have a password')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GenderChoice = (
        ('M', "Male"),
        ('F', "Female"),
    )
    email = models.EmailField(max_length=30, unique=True)
    is_active = models.BooleanField(default=False)
    phone = models.CharField(max_length=13, unique=True)
    nickname = models.CharField(max_length=12)
    birthday = models.DateField(max_length=8, null=True, blank=True)
    gender = models.CharField(choices=GenderChoice)
    is_owner = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

