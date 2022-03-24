from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class GruposAtendimento(models.Model):

    nome = models.CharField('Nome', max_length=300)
    codigo = models.CharField('Codigo', null=True, max_length=20)

    def __str__(self):
        return self.nome

class UsuarioManager(BaseUserManager):
    
    use_in_migrations = True

    def _create_user(self, cpf, password, **extra_fields):
        if not cpf:
            raise ValueError('o CPF é obrigatório!')
        user = self.model(cpf=cpf, username=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(cpf, password, **extra_fields)

    def create_superuser(self, cpf, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
           raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
           raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(cpf, password, **extra_fields)

class CustomUsuario(AbstractUser):

    cpf = models.CharField('CPF', max_length=14, unique=True)
    nascimento = models.DateField('Nascimento', null=False)
    is_staff = models.BooleanField('Paciente', default=True)
    teve_cvd = models.BooleanField('Teve covid nos últimos 30 dias?', default=False)
    id_gp = models.ForeignKey(GruposAtendimento, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'nascimento',]

    def __str__(self):
        return self.first_name

    objects = UsuarioManager()


