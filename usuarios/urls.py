from django.urls import path

from .views import (
    autocadastro,
)

urlpatterns = [
    path('autocadastro/', autocadastro, name='autocadastro'),
]