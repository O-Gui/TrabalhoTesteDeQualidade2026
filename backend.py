from fastapi import FastAPI, Response
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Paciente(BaseModel):
    nome: str
    idade: int
    necessidadePrincipal: str

class Servico(BaseModel):
    idProfissional: str
    titulo: str
    precoTurno: float

@app.post("/pacientes")
def cadastrar_paciente(paciente: Paciente, response: Response):
    if paciente.idade < 0:
        response.status_code = 400
        return {"status": "erro", "mensagem": "Idade inválida"}
    if paciente.idade < 60:
        response.status_code = 400
        return {"status": "erro", "mensagem": "A idade mínima para cadastro é 60 anos"}
    
    response.status_code = 201
    return {"status": "sucesso", "mensagem": "Registrado com sucesso"}

@app.post("/servicos")
def publicar_servico(servico: Servico, response: Response):
    if servico.precoTurno < 50.00 or servico.precoTurno > 500.00:
        response.status_code = 400
        return {"status": "erro", "mensagem": "O valor deve ser entre R$ 50,00 e R$ 500,00"}
    
    response.status_code = 201
    return {"status": "sucesso", "mensagem": "Serviço publicado com sucesso"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
