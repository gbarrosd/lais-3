from django.urls import path

from .views import (
    dashboard,
    listagem_exames,
    pre_agendamento,
    agendar,
    listagem_exames,
    listagem_estab,
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('pre_agendamento/<int:id>/', pre_agendamento, name='pre_agendamento'),
    path('agendar/', agendar, name='agendar'),
    path('listagem_exames/<int:id>/', listagem_exames, name='listagem_exames'),
    path('listagem_estab/', listagem_estab, name='listagem_estab'),
]