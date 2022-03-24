from tkinter import CASCADE
from django.db import models

from usuarios.models import CustomUsuario


class Estabelecimento(models.Model):
    co_cnes = models.CharField('CNES', max_length=15, unique=True, null=False)
    no_fantasia = models.CharField('Nome fantasia', max_length=150)

    REQUIRED_FIELDS = ['co_cnes', 'no_fantasia']

    def __str__(self):
        return self.no_fantasia

class Agendamento(models.Model):
    usuario = models.ForeignKey(CustomUsuario, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    dia_semana = models.CharField(null=False, max_length=15)
    data = models.DateField(null=False)
    hora = models.TimeField(null=False)
    exame = models.BooleanField(null=True, default=False)

    