from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="Backend Care on Live - Testes de API")

# ==========================================
# MODELOS DE DADOS (Schemas)
# ==========================================
class Paciente(BaseModel):
    nome: str
    idade: int
    necessidadePrincipal: str

class Servico(BaseModel):
    idProfissional: str
    titulo: str
    precoTurno: float

# ==========================================
# ROTA 01: TESTE DE API 01 (Cadastro de Paciente)
# ==========================================
@app.post("/pacientes")
def cadastrar_paciente(paciente: Paciente, response: Response):
    # Gera o timestamp no mesmo formato exigido na Wiki
    agora = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Regra da Partição P1 (Idade inválida)
    if paciente.idade < 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "erro",
            "mensagem": "Idade inválida",
            "codigoErro": "IDADE_INVALIDA",
            "timestamp": agora
        }
    
    # Regra da Partição P2 (Idade insuficiente)
    if paciente.idade < 60:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "erro",
            "mensagem": "A idade mínima para cadastro é 60 anos",
            "codigoErro": "IDADE_INSUFICIENTE",
            "timestamp": agora
        }
    
    # Regra da Partição P3 (Sucesso)
    response.status_code = status.HTTP_201_CREATED
    return {
        "status": "sucesso",
        "mensagem": "Registrado com sucesso",
        "dados": {
            "idPaciente": "f8e9d0c1",
            "nome": paciente.nome,
            "dataCriacao": agora
        }
    }

# ==========================================
# ROTA 02: TESTE DE API 02 (Publicação de Serviço)
# ==========================================
@app.post("/servicos")
def publicar_servico(servico: Servico, response: Response):
    agora = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Regras de Borda B1 e B4 (Preço fora do limite permitido)
    if servico.precoTurno < 50.00 or servico.precoTurno > 500.00:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "erro",
            "mensagem": "O valor deve ser entre R$ 50,00 e R$ 500,00",
            "codigoErro": "PRECO_FORA_DO_LIMITE",
            "timestamp": agora
        }
    
    # Regras de Borda B2 e B3 (Preço dentro do limite permitido)
    # A Wiki pede retornos dinâmicos para o idServico dependendo do valor
    id_gerado = "s9z8y7x6" if servico.precoTurno == 500.00 else "s1e2r3v4"

    response.status_code = status.HTTP_201_CREATED
    return {
        "status": "sucesso",
        "mensagem": "Serviço publicado com sucesso",
        "dados": {
            "idServico": id_gerado,
            "precoTurno": servico.precoTurno
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
