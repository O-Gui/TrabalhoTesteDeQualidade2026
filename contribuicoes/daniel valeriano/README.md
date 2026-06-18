# Daniel Valeriano - Testes de Cadastro e Pacientes

Branch sugerida:

```powershell
testes-daniel-valeriano-cadastro-pacientes
```

## Teste de API 01 - Cadastro de Usuario

Tecnica: Tabela de decisao.

| Cenario | Entrada | Resultado esperado |
|---|---|---|
| Cadastro valido | Nome, email, senha e perfil publico | Cadastro realizado com sucesso |
| Email repetido | Email ja cadastrado | Email ja cadastrado |
| Perfil administrador | Perfil administrador pelo cadastro publico | Perfil invalido |

Endpoint:

`POST /api/cadastro`

## Teste de API 02 - Cadastro de Paciente

Tecnica: Analise de valor limite.

| Cenario | Idade | Resultado esperado |
|---|---:|---|
| Idade negativa | -5 | IDADE_INVALIDA |
| Idade insuficiente | 55 | IDADE_INSUFICIENTE |
| Idade valida | 75 | Registrado com sucesso |

Endpoint:

`POST /pacientes`

## Teste de Interface 01 - Cadastro

Tela:

`http://localhost:3000/cadastro`

Validacoes:

- Deve exibir Cadastro Care on Live.
- Deve exibir tipo de usuario.
- Deve permitir selecionar paciente, familiar ou profissional.
- Deve bloquear senha curta.

## Teste de Interface 02 - Painel do Paciente

Tela:

`http://localhost:3000/paciente`

Validacoes:

- Deve exibir Painel do paciente.
- Deve exibir Meus medicamentos.
- Deve exibir Registrar tomada.
- Deve exibir Hora da tomada no modal.

## Arquivos

- `daniel_valeriano_api_postman.json`
- `daniel_valeriano_interface.robot`

## Comandos

```powershell
python run_all.py
robot "contribuicoes\daniel valeriano\daniel_valeriano_interface.robot"
```

