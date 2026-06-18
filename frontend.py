from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/login", response_class=HTMLResponse)
def tela_login():
    return """
    <html>
        <body>
            <h2>Login Care on Live</h2>
            <input type="text" id="email" placeholder="Email" />
            <input type="password" id="senha" placeholder="Senha" />
            <button id="btnEntrar" onclick="validarLogin()">Entrar</button>
            <div id="toast-mensagem"></div>

            <script>
                function validarLogin() {
                    var email = document.getElementById('email').value;
                    var senha = document.getElementById('senha').value;
                    var msg = document.getElementById('toast-mensagem');
                    
                    if (!email) { msg.innerText = 'Email obrigatório'; }
                    else if (!senha) { msg.innerText = 'Senha obrigatória'; }
                    else if (email === 'cuidador@careonlive.com' && senha === 'senhaSegura123') { msg.innerText = 'Login realizado com sucesso'; }
                    else { msg.innerText = 'Credenciais inválidas'; }
                }
            </script>
        </body>
    </html>
    """

@app.get("/pacientes/rotina/medicamento", response_class=HTMLResponse)
def tela_medicamento():
    return """
    <html>
        <body>
            <h2>Cadastro de Medicamento</h2>
            <input type="text" id="nomeRemedio" placeholder="Nome do Remédio" />
            <input type="text" id="horarioRemedio" placeholder="00:00" />
            <input type="number" id="quantidadeRemedio" placeholder="Qtd" />
            <button id="btnSalvarMedicamento" onclick="validarMedicamento()">Salvar</button>
            <div id="alertaFormulario"></div>

            <script>
                function validarMedicamento() {
                    var nome = document.getElementById('nomeRemedio').value;
                    var horario = document.getElementById('horarioRemedio').value;
                    var qtd = document.getElementById('quantidadeRemedio').value;
                    var msg = document.getElementById('alertaFormulario');
                    
                    if (!nome) { msg.innerText = 'Nome do medicamento obrigatório'; }
                    else if (!horario) { msg.innerText = 'Horário obrigatório'; }
                    else if (qtd <= 0) { msg.innerText = 'A quantidade deve ser maior que zero'; }
                    else { msg.innerText = 'Medicação salva na rotina'; }
                }
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)
