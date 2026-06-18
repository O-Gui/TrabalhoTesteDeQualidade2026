# Guilherme Basilio - Testes de Servicos e Admin

Branch sugerida:

```powershell
testes-guilherme-basilio-servicos-admin
```

## Teste de API 01 - Publicacao de Servico

Tecnica: Analise de valor limite.

| Valor | Resultado esperado |
|---:|---|
| 49.99 | PRECO_FORA_DO_LIMITE |
| 50.00 | Servico publicado com sucesso |
| 500.00 | Servico publicado com sucesso |
| 500.01 | PRECO_FORA_DO_LIMITE |

Endpoint:

`POST /servicos`

## Teste de API 02 - Alertas

Tecnica: Validacao de contrato.

Endpoint:

`GET /alertas`

Validacoes:

- Status HTTP 200.
- Campo `total`.
- Campo `dados` como lista.

## Teste de Interface 01 - Painel Profissional

Tela:

`http://localhost:3000/profissional`

Validacoes:

- Deve exibir solicitacoes de servico.
- Deve exibir botoes Aceitar e Recusar.
- Deve exibir Meus pacientes.

## Teste de Interface 02 - Painel Admin

Tela:

`http://localhost:3000/admin`

Validacoes:

- Deve exibir Usuarios cadastrados.
- Deve exibir Servicos publicados.
- Deve exibir Medicamentos registrados.
- Deve exibir Alertas e ocorrencias.

## Arquivos

- `guilherme_basilio_api_postman.json`
- `guilherme_basilio_interface.robot`

## Comandos

```powershell
python run_all.py
robot "contribuicoes\guilherme basilio\guilherme_basilio_interface.robot"
```

