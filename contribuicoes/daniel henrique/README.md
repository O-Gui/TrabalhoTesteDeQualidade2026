# Pessoa 1 - Testes de Login e Profissionais

Branch sugerida:

```powershell
git checkout -b testes-pessoa-1-login-profissionais
```

## Teste de API 01 - Login

### Modelagem

Tecnica utilizada: Particionamento de equivalencia.

| Particao | Entrada | Resultado esperado |
|---|---|---|
| Credenciais validas | Email e senha cadastrados | Login realizado com sucesso |
| Credenciais invalidas | Email ou senha inexistentes | Credenciais invalidas |

### Endpoint

`POST /api/login`

### Requisicao

Headers:

```http
Content-Type: application/json
```

Body valido:

```json
{
  "email": "cuidador@careonlive.com",
  "senha": "senhaSegura123"
}
```

Body invalido:

```json
{
  "email": "erro@careonlive.com",
  "senha": "senhaErrada"
}
```

### Resultado esperado

Caso valido:

```json
{
  "status": "sucesso",
  "mensagem": "Login realizado com sucesso"
}
```

Caso invalido:

```json
{
  "status": "erro",
  "mensagem": "Credenciais invalidas"
}
```

## Teste de API 02 - Profissionais Disponiveis

### Modelagem

Tecnica utilizada: Validacao de contrato.

| Contrato esperado | Resultado esperado |
|---|---|
| Status HTTP | 200 |
| Campo `total` | Deve existir e ser maior ou igual a 4 |
| Campo `dados` | Deve ser uma lista |

### Endpoint

`GET /api/profissionais`

### Resultado esperado

```json
{
  "status": "sucesso",
  "total": 4,
  "dados": []
}
```

## Teste de Interface 01 - Login

### Modelagem

Tecnica utilizada: Particionamento de equivalencia.

| Particao | Acao | Resultado esperado |
|---|---|---|
| Credenciais validas | Informar email e senha do profissional | Login realizado com sucesso |
| Credenciais invalidas | Informar email e senha incorretos | Credenciais invalidas |

### Tela

`http://localhost:3000/login`

### Resultado esperado

- A tela deve exibir `Login Care on Live`.
- O login valido deve apresentar `Login realizado com sucesso`.
- O login invalido deve apresentar `Credenciais invalidas`.

## Teste de Interface 02 - Profissionais Disponiveis

### Modelagem

Tecnica utilizada: Validacao funcional.

| Validacao | Resultado esperado |
|---|---|
| Abrir tela de profissionais | Status visual carregado |
| Titulo da pagina | Deve conter `Profissionais disponiveis` |
| Acao principal | Deve conter `Selecionar profissional` |

### Tela

`http://localhost:3000/profissionais`

### Resultado esperado

- A tela deve abrir corretamente.
- Deve exibir profissionais disponiveis.
- Deve exibir a acao `Selecionar profissional`.

## Arquivos da Pessoa 1

- `pessoa1_api_postman.json`: colecao Postman com os testes de API.
- `pessoa1_interface.robot`: suite Robot Framework com os testes de interface.

## Comandos

Para rodar a aplicacao:

```powershell
python run_all.py
```

Para executar a suite Robot da Pessoa 1:

```powershell
robot contribuicoes\pessoa1\pessoa1_interface.robot
```

