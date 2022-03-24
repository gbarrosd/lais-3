from django.contrib import messages
from datetime import datetime

from django.shortcuts import redirect, render
import re

from usuarios.models import GruposAtendimento
from .forms import CustomUsuarioCreateForm

def autocadastro(request):
    if request.method == "GET":
        form = CustomUsuarioCreateForm()
        context = {
            "form":form,
        }
        return render(request, 'formCadastro.html', context=context)
    else:
        dados = request.POST.copy()
        cpf = re.sub(r'[a-zA-Z^Çç./*@$%()+#!?\]\[_&\'\s"=~|,ªº-]', '', request.POST['cpf'])
        dados['cpf'] = cpf
        form = CustomUsuarioCreateForm(dados)
        if form.is_valid():
            form.save()
            data_nascimento = request.POST['nascimento']
            data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
            data_hoje = datetime.today()
            idade = data_hoje.year - data_nascimento.year - ((data_hoje.month, data_hoje.day) < 
                (data_nascimento.month, data_nascimento.day))
            co_gp = GruposAtendimento.objects.get(pk=request.POST['id_gp'])
            cvd = request.POST.get('teve_cvd')
            if  cvd == 'on' or idade < 18 or co_gp.codigo == '001501' or co_gp.codigo == '001101' or co_gp.codigo == '000205':
                messages.warning(request, 'Você não está apto para participar!')
                return redirect('login')
            else:
                messages.success(request, 'Você está apto para participar!')
                return redirect('login')

        form = CustomUsuarioCreateForm(dados)
        context = {
            "form": form
        }
        return render(request, 'formCadastro.html', context)
