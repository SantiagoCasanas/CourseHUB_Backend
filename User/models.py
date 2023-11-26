from datetime import timezone
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not (email or username):
            raise ValueError('Email and username are required')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            **extra_fields
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', unique=True, max_length=100, null=False)
    email = models.EmailField('Email', unique=True, max_length=100, null=False)
    full_name = models.CharField('Full name', max_length=200, null=False)
    password = models.CharField(
                                max_length=200,
                                validators=[validators.MinLengthValidator(8)])
    is_active = models.BooleanField(default=True)
    is_temporarily_inactive = models.BooleanField(default=False)
    inactive_timestamp = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']
    objects = UserManager()

    class Meta:
        unique_together = ('email', 'is_active')

    def __str__(self):
        return f'User: {self.username}'
    
    def set_temporarily_inactive(self, minutes=30):
        self.is_temporarily_inactive = True
        self.inactive_timestamp = timezone.now() + timezone.timedelta(minutes=minutes)
        self.save()

    def is_temporaly_inactive(self):
        if self.is_temporarily_inactive and self.inactive_timestamp > timezone.now():
            self.is_temporarily_inactive = False
            self.inactive_timestamp = None
            self.save()
            return False
        return self.is_temporarily_inactive
