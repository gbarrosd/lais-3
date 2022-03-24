import json

modelo = [
    {
        "model": "core.Estabelecimento",
        "fields": {
            "co_cnes": "3154408",
            "no_fantasia": "CLINICA DE ENDOCRINOLOGIA E PEDIATRIA"
        }
    }
]

with open('core/fixtures/estabelecimentos_pr.json', 'r') as estab:
    dados_json = estab.read()
    dados = json.loads(dados_json)
    modelo_json = list()
    for data in dados.get('estabelecimento'):
        modelo = {
                "model": "core.Estabelecimento",
                "fields": {
                    "co_cnes": data.get('co_cnes'),
                    "no_fantasia": data.get('no_fantasia')
                }
            }
        modelo_json.append(modelo)
    with open('core/fixtures/estab_data.json', 'w') as estab_w:
        json_test = json.dumps(modelo_json)
        json_w = estab_w.write(json_test)
