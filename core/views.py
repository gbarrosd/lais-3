from datetime import datetime
import pandas as pd
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import Agendar
from .models import Estabelecimento, Agendamento
from usuarios.models import CustomUsuario

@login_required
def dashboard(request):
    id_usuario = request.user.id
    usuario = CustomUsuario.objects.get(pk=id_usuario)
    data_nascimento = usuario.nascimento
    data_hoje = datetime.today()
    idade = data_hoje.year - data_nascimento.year - ((data_hoje.month, data_hoje.day) < 
         (data_nascimento.month, data_nascimento.day))
    if usuario.id_gp:
        codigo = usuario.id_gp.codigo
    else:
        codigo = '0'

    if usuario.teve_cvd or idade < 18 or codigo == '001101' or codigo == '001501' or codigo == '000205':
        apto = 'Não'
    else: 
        apto = 'Sim'
    context = {
        'idade': idade,
        'apto': apto
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def pre_agendamento(request, id):
    _usuario = CustomUsuario.objects.get(pk=id)
    data_nascimento = _usuario.nascimento
    data_hoje = datetime.today()
    idade = data_hoje.year - data_nascimento.year - ((data_hoje.month, data_hoje.day) < 
         (data_nascimento.month, data_nascimento.day))
    if _usuario.id_gp:
        codigo = _usuario.id_gp.codigo
    else:
        codigo = '0'

    if _usuario.teve_cvd or idade < 18 or codigo == '001101' or codigo == '001501' or codigo == '000205':
        messages.warning(request, 'Você não é do grupo alvo!')
        return redirect('dashboard')
    else:
        try: 
            Agendamento.objects.get(usuario=id, exame=False) 
            messages.warning(request, 'Você já tem um exame marcado!')
            return redirect('dashboard')
        except Agendamento.DoesNotExist:
            estabelecimento = Estabelecimento.objects.all()
            usuario = CustomUsuario.objects.get(pk=id)
            data_nascimento = usuario.nascimento
            data_hoje = datetime.today()
            idade = data_hoje.year - data_nascimento.year - ((data_hoje.month, data_hoje.day) < 
                (data_nascimento.month, data_nascimento.day))
            context = {
                'id':id,
                'estabelecimento':estabelecimento,
                'idade':idade,
                'apto': 'Sim',
            }
            return render(request, 'core/pre_agendamento.html', context)

@login_required
def agendar(request):
    if (request.POST['aux'] == '1'):
        usuario = request.POST['usuario']
        no_dia = pd.Timestamp(request.POST['data_exame']).day_name()
        nome_dias = {
            'Wednesday':'Quarta-Feira',
            'Thursday':'Quinta-Feira',
            'Friday':'Sexta-Feira',
            'Saturday':'Sabado'
        }
        data = datetime.strptime(request.POST['data_exame'], '%Y-%m-%d')
        if data < datetime.today():
            messages.warning(request, 'Porfavor, selecione uma data futura!')
            return redirect('pre_agendamento', usuario)
        elif no_dia == 'Sunday' or no_dia == 'Monday' or no_dia == 'Tuesday':
            messages.warning(request, 'Agendamentos apenas de quarta á sabado!')
            return redirect('pre_agendamento', usuario)
        no_dia_semana = nome_dias[no_dia]
        data = request.POST['data_exame']
        data = datetime.strptime(data, '%Y-%m-%d').date()
        data = '{}/{}/{}'.format(data.day, data.month,
        data.year)
        estabelecimento = request.POST['estabelecimento']
        no_estabelecimento = Estabelecimento.objects.get(pk=estabelecimento)
        idade = request.POST['idade']
        form = Agendar()
        context = {
        'form':form,
        'id':usuario,
        'dia':no_dia_semana,
        'data':data,
        'no_estabelecimento':no_estabelecimento,
        'estabelecimento':estabelecimento,
        'idade':idade,
        'apto': 'Sim'
        }
        return render(request, 'core/agendar.html', context)
    else:
        form = Agendar(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listagem_exames', request.POST['usuario'])
        # context = {
        #     'form':form,
        #     'id':id,
        #     'estabelecimento':estabelecimento,
        # }
        return render(request, 'core/agendar.html', context=context)
    return render(request, 'core/agendar.html')

@login_required
def listagem_exames(request, id):
    exames = Agendamento.objects.filter(usuario=id).order_by('-data')

    context = {
        'exames': exames,
        'apto': 'Sim'
    }
    return render(request, 'core/listagem_exames.html', context)

@login_required
def listagem_estab(request):
    if request.user.is_superuser:
        search = request.GET.get('search')
        if search:
            estab_nome = Estabelecimento.objects.filter(no_fantasia__icontains=search)
            estab_co = Estabelecimento.objects.filter(co_cnes__icontains=search)
            estabelecimentos = estab_nome.union(estab_co)
            context = {
                'estabelecimentos':estabelecimentos
            }
        else:
            estabelecimentos = Estabelecimento.objects.all()
            context = {
                'estabelecimentos':estabelecimentos
            }
        return render(request, 'core/admin/listagem_estab.html', context)
    else:
        messages.warning(request, 'Você não é usuário administrador!')
        return redirect('dashboard')
