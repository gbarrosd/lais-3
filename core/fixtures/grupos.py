import json
from tkinter.tix import INCREASING

from numpy import isin

with open('core/fixtures/grupos_atendimento.json', 'r') as grupo:
    dados_json = grupo.read()
    dados = json.loads(dados_json)
    modelo_json = list()
    for data in dados.get('grupos').get('grupoatendimento'):
        modelo = {
                "model": "usuarios.GruposAtendimento",
                "fields": {
                    "nome": data.get('nome'),
                    "codigo": data.get('codigo_si_pni') if not isinstance(data.get('codigo_si_pni'), dict) else None
                }
            }
        modelo_json.append(modelo)
    with open('core/fixtures/grupos_data.json', 'w') as grupo_w:
        json_test = json.dumps(modelo_json, indent=4, ensure_ascii=False)
        json_w = grupo_w.write(json_test)
