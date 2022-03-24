from datetime import datetime
from logging import raiseExceptions
from django import forms

from localflavor.br.forms import BRCPFField

from .models import CustomUsuario

class CustomUsuarioCreateForm(forms.ModelForm):
    cpf = BRCPFField()

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput)

    class Meta:
        model = CustomUsuario
        fields = (
            'first_name',
            'last_name',
            'nascimento',
            'cpf',
            'id_gp',
            'teve_cvd',
            'password1',
            'password2',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não combinam!")
        return password2

    def nascimento(self):
        nascimento = str(self.nascimento)
        data = datetime.strptime(nascimento, '%Y/%m/%d')
        if data < datetime.today():
            print(data)
            raise forms.ValidationError('Informe uma data válida!')
        print(data)
        return self.nascimento
    
    def save(self, commit=True):
        # self.nascimento()
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.cpf = self.cleaned_data["username"]
        user.username = user.cpf
        if commit:
            user.save()
        return user
        