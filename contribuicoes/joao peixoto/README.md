# Joao Peixoto - Testes de Medicamentos e SOS

Branch:

```powershell
testes-joao-peixoto-medicamentos-sos
```

## Teste de API 01 - Cadastro de Medicamento

### Modelagem

Tecnica utilizada: Particionamento de equivalencia.

| Particao | Entrada | Resultado esperado |
|---|---|---|
| Dados validos | Nome, horario e quantidade maior que zero | Medicacao salva na rotina |
| Quantidade zerada | Quantidade igual a 0 | A quantidade deve ser maior que zero |
| Quantidade negativa | Quantidade menor que 0 | A quantidade deve ser maior que zero |

### Endpoint

`POST /medicamentos`

### Requisicao valida

```json
{
  "paciente": "Maria de Lourdes",
  "nomeRemedio": "Losartana 50mg",
  "horarioRemedio": "08:00",
  "quantidadeRemedio": 1
}
```

### Resultado esperado

Status HTTP: `201`

```json
{
  "status": "sucesso",
  "mensagem": "Medicação salva na rotina"
}
```

## Teste de API 02 - Acionamento de SOS

### Modelagem

Tecnica utilizada: Fluxo principal.

| Fluxo | Entrada | Resultado esperado |
|---|---|---|
| SOS valido | Paciente e localizacao preenchidos | SOS acionado e familia notificada |

### Endpoint

`POST /sos`

### Requisicao

```json
{
  "paciente": "Maria de Lourdes",
  "localizacao": "Residencia"
}
```

### Resultado esperado

Status HTTP: `201`

```json
{
  "status": "sucesso",
  "mensagem": "SOS acionado e familia notificada"
}
```

## Teste de Interface 01 - Cadastro de Medicamento

### Modelagem

Tecnica utilizada: Tabela de decisao.

| Nome | Horario | Quantidade | Resultado esperado |
|---|---|---|---|
| Preenchido | Preenchido | Maior que zero | Medicacao salva na rotina |
| Vazio | Preenchido | Maior que zero | Nome do medicamento obrigatorio |
| Preenchido | Vazio | Maior que zero | Horario obrigatorio |
| Preenchido | Preenchido | Zero | A quantidade deve ser maior que zero |

### Tela

`http://localhost:3000/pacientes/rotina/medicamento`

## Teste de Interface 02 - Painel Familiar

### Modelagem

Tecnica utilizada: Validacao funcional.

| Validacao | Resultado esperado |
|---|---|
| Abrir painel familiar | Deve exibir Painel do familiar |
| Medicamentos do paciente | Deve exibir Tomou? e Hora registrada |
| Registro de tomada | Deve exibir botao Registrar tomada |
| Modal de tomada | Deve exibir Hora da tomada |

### Tela

`http://localhost:3000/familiar`

## Arquivos

- `joao_peixoto_api_postman.json`
- `joao_peixoto_interface.robot`

## Comandos

Para rodar a aplicacao:

```powershell
python run_all.py
```

Para executar os testes Robot:

```powershell
robot "contribuicoes\joao peixoto\joao_peixoto_interface.robot"
```

