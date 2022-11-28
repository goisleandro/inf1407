from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MeuAdministradorConta(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Usuarios precisam ter um email!")
        if not username:
            raise ValueError("Usuarios precisam ter um username!")

        usuario = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, username, password):
        usuario = self.create_user(
                email = self.normalize_email(email),
                password = password,
                username = username,
        )
        usuario.is_admin = True
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario


class Conta(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='data de entrada', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='ultimo login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nome = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MeuAdministradorConta()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True    