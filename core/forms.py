from django import forms

from .models import (
    Agendamento,
)

class Agendar(forms.ModelForm):
    
    class Meta:
        model = Agendamento
        fields = (
            'dia_semana',
            'data',
            'estabelecimento',
            'usuario',
            'hora'
        )