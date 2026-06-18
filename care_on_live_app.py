from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, Response, status
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field


app = FastAPI(
    title="Care on Live",
    description="Plataforma academica para gestao e monitoramento de cuidados com idosos.",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent


class Paciente(BaseModel):
    nome: str = Field(min_length=1)
    idade: int
    necessidadePrincipal: str = Field(min_length=1)


class Servico(BaseModel):
    idProfissional: str = Field(min_length=1)
    titulo: str = Field(min_length=1)
    precoTurno: float


class Login(BaseModel):
    email: str
    senha: str


class Medicamento(BaseModel):
    nomeRemedio: str = Field(min_length=1)
    horarioRemedio: str = Field(min_length=1)
    quantidadeRemedio: int
    paciente: str = "Maria de Lourdes"


class Sos(BaseModel):
    paciente: str = "Maria de Lourdes"
    localizacao: Optional[str] = "Residencia"
    descricao: Optional[str] = "Acionamento manual pelo cuidador"


PROFISSIONAIS = [
    {
        "idProfissional": "prof001",
        "nome": "Ana Paula Ribeiro",
        "registro": "COREN-DF-12345",
        "especialidade": "Cuidadora de idosos",
        "turno": "Noturno",
        "status": "Disponivel",
        "pacientesAtendidos": 3,
        "cidade": "Brasilia - DF",
        "avaliacao": 4.9,
        "precoTurno": 180.0,
        "resumo": "Experiencia com rotina noturna, medicacao e acompanhamento de idosos com risco alto.",
    },
    {
        "idProfissional": "prof002",
        "nome": "Bruno Almeida Costa",
        "registro": "COREN-GO-73421",
        "especialidade": "Tecnico de enfermagem",
        "turno": "Diurno",
        "status": "Em atendimento",
        "pacientesAtendidos": 2,
        "cidade": "Aguas Claras - DF",
        "avaliacao": 4.7,
        "precoTurno": 220.0,
        "resumo": "Tecnico de enfermagem para controle de sinais vitais, glicemia e pressao.",
    },
    {
        "idProfissional": "prof003",
        "nome": "Camila Nascimento",
        "registro": "FISIO-DF-55210",
        "especialidade": "Fisioterapia motora",
        "turno": "Vespertino",
        "status": "Disponivel",
        "pacientesAtendidos": 4,
        "cidade": "Taguatinga - DF",
        "avaliacao": 4.8,
        "precoTurno": 160.0,
        "resumo": "Atendimento domiciliar com foco em mobilidade, fisioterapia e prevencao de quedas.",
    },
    {
        "idProfissional": "prof004",
        "nome": "Diego Martins Rocha",
        "registro": "COREN-DF-99812",
        "especialidade": "Enfermagem domiciliar",
        "turno": "Plantonista",
        "status": "Indisponivel",
        "pacientesAtendidos": 1,
        "cidade": "Guara - DF",
        "avaliacao": 4.6,
        "precoTurno": 250.0,
        "resumo": "Enfermagem domiciliar para pos-cirurgico e acompanhamento intensivo.",
    },
]

PACIENTES = [
    {
        "idPaciente": "p001",
        "nome": "Maria de Lourdes",
        "idade": 75,
        "necessidadePrincipal": "Monitoramento continuo SOS",
        "cuidador": "Ana Paula Ribeiro",
        "risco": "Alto",
        "status": "Em acompanhamento",
        "dataCriacao": "2026-06-18T09:00:00Z",
    },
    {
        "idPaciente": "p002",
        "nome": "Jose Carlos Pereira",
        "idade": 82,
        "necessidadePrincipal": "Controle de glicemia e pressao",
        "cuidador": "Bruno Almeida Costa",
        "risco": "Medio",
        "status": "Rotina ativa",
        "dataCriacao": "2026-06-18T09:10:00Z",
    },
    {
        "idPaciente": "p003",
        "nome": "Helena Duarte Lima",
        "idade": 69,
        "necessidadePrincipal": "Fisioterapia e lembretes de medicacao",
        "cuidador": "Camila Nascimento",
        "risco": "Baixo",
        "status": "Rotina ativa",
        "dataCriacao": "2026-06-18T09:20:00Z",
    },
    {
        "idPaciente": "p004",
        "nome": "Antonio Silva Ramos",
        "idade": 88,
        "necessidadePrincipal": "Acompanhamento pos-cirurgico",
        "cuidador": "Diego Martins Rocha",
        "risco": "Alto",
        "status": "Atencao intensiva",
        "dataCriacao": "2026-06-18T09:30:00Z",
    },
    {
        "idPaciente": "p005",
        "nome": "Tereza Cristina Moura",
        "idade": 73,
        "necessidadePrincipal": "Rotina de hidratacao e mobilidade",
        "cuidador": "Ana Paula Ribeiro",
        "risco": "Medio",
        "status": "Em acompanhamento",
        "dataCriacao": "2026-06-18T09:40:00Z",
    },
]

SERVICOS = [
    {
        "idServico": "s001",
        "idProfissional": "COREN-DF-12345",
        "titulo": "Cuidador noturno",
        "precoTurno": 180.0,
        "status": "Publicado",
    },
    {
        "idServico": "s002",
        "idProfissional": "COREN-GO-73421",
        "titulo": "Acompanhamento diurno",
        "precoTurno": 220.0,
        "status": "Publicado",
    },
    {
        "idServico": "s003",
        "idProfissional": "FISIO-DF-55210",
        "titulo": "Fisioterapia domiciliar",
        "precoTurno": 160.0,
        "status": "Publicado",
    },
]

MEDICAMENTOS = [
    {
        "idMedicamento": "m001",
        "paciente": "Maria de Lourdes",
        "nomeRemedio": "Losartana 50mg",
        "horarioRemedio": "08:00",
        "quantidadeRemedio": 1,
        "status": "Agendado",
    },
    {
        "idMedicamento": "m002",
        "paciente": "Jose Carlos Pereira",
        "nomeRemedio": "Metformina 850mg",
        "horarioRemedio": "12:00",
        "quantidadeRemedio": 1,
        "status": "Agendado",
    },
    {
        "idMedicamento": "m003",
        "paciente": "Helena Duarte Lima",
        "nomeRemedio": "Vitamina D",
        "horarioRemedio": "09:30",
        "quantidadeRemedio": 1,
        "status": "Agendado",
    },
    {
        "idMedicamento": "m004",
        "paciente": "Antonio Silva Ramos",
        "nomeRemedio": "Anticoagulante",
        "horarioRemedio": "20:00",
        "quantidadeRemedio": 1,
        "status": "Pendente",
    },
]

ALERTAS = [
    {
        "idAlerta": "a001",
        "tipo": "medicamento",
        "mensagem": "Losartana 50mg agendada para 08:00",
        "status": "ativo",
    }
]

USUARIOS = {
    "admin@careonlive.com": {
        "senha": "admin123",
        "perfil": "administrador",
        "nome": "Administrador Care on Live",
        "dashboard": "/admin",
    },
    "cuidador@careonlive.com": {
        "senha": "senhaSegura123",
        "perfil": "profissional",
        "nome": "Cuidador demonstracao",
        "dashboard": "/profissional",
    },
    "paciente@careonlive.com": {
        "senha": "paciente123",
        "perfil": "paciente",
        "nome": "Maria de Lourdes",
        "dashboard": "/paciente",
    },
    "familiar@careonlive.com": {
        "senha": "familiar123",
        "perfil": "familiar",
        "nome": "Responsavel familiar",
        "dashboard": "/familiar",
    },
}


def agora_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pagina_base(titulo: str, conteudo: str) -> str:
    return f"""
    <!doctype html>
    <html lang="pt-BR">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{titulo} - Care on Live</title>
        <style>
            :root {{
                --bg: #f4f7f8;
                --surface: #ffffff;
                --surface-soft: #eef5f3;
                --text: #172126;
                --muted: #65747b;
                --line: #d7e2e2;
                --primary: #087f8c;
                --primary-dark: #05626d;
                --danger: #b42318;
                --success: #087443;
                --warning: #996f00;
                --accent: #324376;
            }}
            * {{
                box-sizing: border-box;
            }}
            body {{
                margin: 0;
                min-height: 100vh;
                background: var(--bg);
                color: var(--text);
                font-family: Arial, Helvetica, sans-serif;
                letter-spacing: 0;
            }}
            header {{
                background: var(--surface);
                border-bottom: 1px solid var(--line);
                position: sticky;
                top: 0;
                z-index: 5;
            }}
            .topbar {{
                width: min(1180px, calc(100% - 32px));
                min-height: 68px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
            }}
            .brand {{
                display: flex;
                align-items: center;
                gap: 12px;
                min-width: 210px;
            }}
            .brand-mark {{
                width: 38px;
                height: 38px;
                border-radius: 8px;
                background: var(--primary);
                color: #fff;
                display: grid;
                place-items: center;
                font-weight: 700;
            }}
            .brand strong {{
                display: block;
                font-size: 18px;
            }}
            .brand span {{
                display: block;
                color: var(--muted);
                font-size: 12px;
                margin-top: 2px;
            }}
            nav {{
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                justify-content: flex-end;
            }}
            nav a {{
                color: var(--text);
                text-decoration: none;
                border: 1px solid var(--line);
                background: #fff;
                border-radius: 8px;
                min-height: 38px;
                padding: 10px 12px;
                font-size: 14px;
            }}
            nav a:hover {{
                border-color: var(--primary);
                color: var(--primary-dark);
            }}
            main {{
                width: min(1180px, calc(100% - 32px));
                margin: 22px auto 40px;
            }}
            .grid {{
                display: grid;
                gap: 16px;
            }}
            .grid-2 {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
            .grid-3 {{
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }}
            .panel, .card {{
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: 8px;
            }}
            .panel {{
                padding: 20px;
            }}
            .card {{
                padding: 16px;
            }}
            .section-title {{
                margin: 0 0 12px;
                font-size: 20px;
            }}
            .muted {{
                color: var(--muted);
            }}
            .metric {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 14px;
                min-height: 88px;
            }}
            .metric strong {{
                display: block;
                font-size: 26px;
                margin-bottom: 4px;
            }}
            .metric span {{
                color: var(--muted);
                font-size: 13px;
            }}
            .icon {{
                width: 44px;
                height: 44px;
                border-radius: 8px;
                display: grid;
                place-items: center;
                background: var(--surface-soft);
                color: var(--primary-dark);
                font-weight: 700;
            }}
            form {{
                display: grid;
                gap: 12px;
            }}
            label {{
                display: grid;
                gap: 6px;
                color: var(--muted);
                font-size: 13px;
            }}
            input, textarea, select {{
                width: 100%;
                min-height: 42px;
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 10px 12px;
                font: inherit;
                background: #fff;
                color: var(--text);
            }}
            textarea {{
                min-height: 92px;
                resize: vertical;
            }}
            button {{
                min-height: 42px;
                border: 0;
                border-radius: 8px;
                padding: 10px 14px;
                background: var(--primary);
                color: #fff;
                font-weight: 700;
                cursor: pointer;
            }}
            button:hover {{
                background: var(--primary-dark);
            }}
            button.secondary {{
                background: var(--accent);
            }}
            button.danger {{
                background: var(--danger);
            }}
            .message {{
                min-height: 24px;
                font-weight: 700;
                color: var(--accent);
            }}
            .message.success {{
                color: var(--success);
            }}
            .message.error {{
                color: var(--danger);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                overflow: hidden;
                border-radius: 8px;
            }}
            th, td {{
                padding: 12px;
                border-bottom: 1px solid var(--line);
                text-align: left;
                vertical-align: top;
            }}
            th {{
                background: var(--surface-soft);
                color: var(--muted);
                font-size: 12px;
                text-transform: uppercase;
            }}
            tr:last-child td {{
                border-bottom: 0;
            }}
            .status {{
                display: inline-flex;
                align-items: center;
                min-height: 24px;
                border-radius: 999px;
                padding: 4px 10px;
                background: #e7f7ef;
                color: var(--success);
                font-size: 12px;
                font-weight: 700;
            }}
            .status.warning {{
                background: #fff5d8;
                color: var(--warning);
            }}
            .marketplace {{
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 16px;
            }}
            .professional-card {{
                display: grid;
                gap: 12px;
                min-height: 280px;
            }}
            .avatar {{
                width: 56px;
                height: 56px;
                border-radius: 8px;
                display: grid;
                place-items: center;
                background: var(--surface-soft);
                color: var(--primary-dark);
                font-size: 20px;
                font-weight: 700;
            }}
            .rating {{
                color: var(--warning);
                font-weight: 700;
            }}
            .price {{
                color: var(--primary-dark);
                font-size: 18px;
                font-weight: 700;
            }}
            .login-layout {{
                display: grid;
                grid-template-columns: minmax(0, 1fr) minmax(320px, 430px);
                gap: 28px;
                align-items: center;
                min-height: calc(100vh - 150px);
            }}
            .login-intro {{
                display: grid;
                gap: 18px;
                align-content: center;
            }}
            .logo-large {{
                width: 104px;
                height: 104px;
                border-radius: 18px;
                background: var(--primary);
                color: #fff;
                display: grid;
                place-items: center;
                font-size: 34px;
                font-weight: 800;
            }}
            .login-intro h1 {{
                margin: 0;
                font-size: 38px;
            }}
            .login-panel {{
                justify-self: end;
                width: 100%;
            }}
            .toolbar {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                align-items: center;
            }}
            @media (max-width: 820px) {{
                .topbar {{
                    align-items: flex-start;
                    flex-direction: column;
                    padding: 14px 0;
                }}
                nav {{
                    justify-content: flex-start;
                }}
                .grid-2, .grid-3 {{
                    grid-template-columns: 1fr;
                }}
                .marketplace {{
                    grid-template-columns: 1fr;
                }}
                .login-layout {{
                    grid-template-columns: 1fr;
                    min-height: auto;
                }}
                .login-panel {{
                    justify-self: stretch;
                }}
                table {{
                    display: block;
                    overflow-x: auto;
                    white-space: nowrap;
                }}
            }}
        </style>
    </head>
    <body>
        <header>
            <div class="topbar">
                <a class="brand" href="/" aria-label="Care on Live">
                    <span class="brand-mark">CL</span>
                    <span>
                        <strong>Care on Live</strong>
                        <span>Gestao de cuidado domiciliar</span>
                    </span>
                </a>
                <nav aria-label="Navegacao principal">
                    <a href="/">Home</a>
                    <a href="/profissionais">Profissionais disponiveis</a>
                    <a href="/login">Login</a>
                    <a href="/pacientes/rotina/medicamento">Medicamentos</a>
                    <a href="/docs">API</a>
                </nav>
            </div>
        </header>
        <main>{conteudo}</main>
    </body>
    </html>
    """


@app.get("/health")
def health():
    return {"status": "online", "servico": "Care on Live", "timestamp": agora_iso()}


@app.get("/acessos-care-on-live.pdf")
@app.get("/static/acessos-care-on-live.pdf")
def pdf_acessos():
    caminho_pdf = BASE_DIR / "docs" / "acessos-care-on-live.pdf"
    return FileResponse(caminho_pdf, media_type="application/pdf", filename="acessos-care-on-live.pdf")


@app.post("/api/login")
def login(credenciais: Login, response: Response):
    if not credenciais.email:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "Email obrigat\u00f3rio"}
    if not credenciais.senha:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "Senha obrigat\u00f3ria"}
    usuario = USUARIOS.get(credenciais.email)
    if usuario and usuario["senha"] == credenciais.senha:
        return {
            "status": "sucesso",
            "mensagem": "Login realizado com sucesso",
            "token": "token-academico-care-on-live",
            "usuario": {
                "nome": usuario["nome"],
                "perfil": usuario["perfil"],
                "dashboard": usuario["dashboard"],
            },
        }
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"status": "erro", "mensagem": "Credenciais inv\u00e1lidas"}


@app.get("/usuarios")
def listar_usuarios():
    dados = [
        {
            "email": email,
            "nome": usuario["nome"],
            "perfil": usuario["perfil"],
            "dashboard": usuario["dashboard"],
        }
        for email, usuario in USUARIOS.items()
    ]
    return {"status": "sucesso", "total": len(dados), "dados": dados}


@app.get("/pacientes")
def listar_pacientes():
    return {"status": "sucesso", "total": len(PACIENTES), "dados": PACIENTES}


@app.get("/api/profissionais")
def listar_profissionais():
    return {"status": "sucesso", "total": len(PROFISSIONAIS), "dados": PROFISSIONAIS}


@app.post("/pacientes")
def cadastrar_paciente(paciente: Paciente, response: Response):
    agora = agora_iso()

    if paciente.idade < 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "erro",
            "mensagem": "Idade inv\u00e1lida",
            "codigoErro": "IDADE_INVALIDA",
            "timestamp": agora,
        }

    if paciente.idade < 60:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "erro",
            "mensagem": "A idade m\u00ednima para cadastro \u00e9 60 anos",
            "codigoErro": "IDADE_INSUFICIENTE",
            "timestamp": agora,
        }

    id_paciente = "f8e9d0c1" if paciente.nome else uuid4().hex[:8]
    registro = {
        "idPaciente": id_paciente,
        "nome": paciente.nome,
        "idade": paciente.idade,
        "necessidadePrincipal": paciente.necessidadePrincipal,
        "cuidador": "A definir",
        "risco": "A avaliar",
        "status": "Cadastro novo",
        "dataCriacao": agora,
    }
    PACIENTES.append(registro)

    response.status_code = status.HTTP_201_CREATED
    return {
        "status": "sucesso",
        "mensagem": "Registrado com sucesso",
        "dados": {
            "idPaciente": registro["idPaciente"],
            "nome": registro["nome"],
            "dataCriacao": registro["dataCriacao"],
        },
    }


@app.get("/servicos")
def listar_servicos():
    return {"status": "sucesso", "total": len(SERVICOS), "dados": SERVICOS}


@app.post("/servicos")
def publicar_servico(servico: Servico, response: Response):
    agora = agora_iso()

    if servico.precoTurno < 50.00 or servico.precoTurno > 500.00:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": "erro",
            "mensagem": "O valor deve ser entre R$ 50,00 e R$ 500,00",
            "codigoErro": "PRECO_FORA_DO_LIMITE",
            "timestamp": agora,
        }

    id_gerado = "s9z8y7x6" if servico.precoTurno == 500.00 else "s1e2r3v4"
    registro = {
        "idServico": id_gerado,
        "idProfissional": servico.idProfissional,
        "titulo": servico.titulo,
        "precoTurno": servico.precoTurno,
        "status": "Publicado",
    }
    SERVICOS.append(registro)

    response.status_code = status.HTTP_201_CREATED
    return {
        "status": "sucesso",
        "mensagem": "Servi\u00e7o publicado com sucesso",
        "dados": {
            "idServico": id_gerado,
            "precoTurno": servico.precoTurno,
        },
    }


@app.get("/medicamentos")
def listar_medicamentos():
    return {"status": "sucesso", "total": len(MEDICAMENTOS), "dados": MEDICAMENTOS}


@app.post("/pacientes/rotina/medicamento")
@app.post("/medicamentos")
def salvar_medicamento(medicamento: Medicamento, response: Response):
    if medicamento.quantidadeRemedio <= 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "A quantidade deve ser maior que zero"}

    registro = {
        "idMedicamento": uuid4().hex[:8],
        "paciente": medicamento.paciente,
        "nomeRemedio": medicamento.nomeRemedio,
        "horarioRemedio": medicamento.horarioRemedio,
        "quantidadeRemedio": medicamento.quantidadeRemedio,
        "status": "Agendado",
    }
    MEDICAMENTOS.append(registro)
    ALERTAS.append(
        {
            "idAlerta": uuid4().hex[:8],
            "tipo": "medicamento",
            "mensagem": f"{registro['nomeRemedio']} agendado para {registro['horarioRemedio']}",
            "status": "ativo",
        }
    )
    response.status_code = status.HTTP_201_CREATED
    return {"status": "sucesso", "mensagem": "Medica\u00e7\u00e3o salva na rotina", "dados": registro}


@app.get("/alertas")
def listar_alertas():
    return {"status": "sucesso", "total": len(ALERTAS), "dados": ALERTAS}


@app.post("/sos")
def acionar_sos(sos: Sos, response: Response):
    alerta = {
        "idAlerta": uuid4().hex[:8],
        "tipo": "SOS",
        "paciente": sos.paciente,
        "localizacao": sos.localizacao,
        "descricao": sos.descricao,
        "timestamp": agora_iso(),
        "status": "critico",
    }
    ALERTAS.append(alerta)
    response.status_code = status.HTTP_201_CREATED
    return {
        "status": "sucesso",
        "mensagem": "SOS acionado e familia notificada",
        "dados": alerta,
    }


@app.get("/painel", response_class=HTMLResponse)
def painel():
    linhas_medicamentos = "".join(
        f"""
        <tr>
            <td>{item['paciente']}</td>
            <td>{item['nomeRemedio']}</td>
            <td>{item['horarioRemedio']}</td>
            <td>{item['quantidadeRemedio']}</td>
            <td><span class="status">{item['status']}</span></td>
        </tr>
        """
        for item in MEDICAMENTOS
    )
    linhas_servicos = "".join(
        f"""
        <tr>
            <td>{item['titulo']}</td>
            <td>{item['idProfissional']}</td>
            <td>R$ {item['precoTurno']:.2f}</td>
            <td><span class="status">{item['status']}</span></td>
        </tr>
        """
        for item in SERVICOS
    )
    conteudo = f"""
    <section class="grid grid-3" aria-label="Resumo operacional">
        <article class="card metric">
            <div>
                <strong>{len(PACIENTES)}</strong>
                <span>pacientes monitorados</span>
            </div>
            <div class="icon">P</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(MEDICAMENTOS)}</strong>
                <span>medicamentos agendados</span>
            </div>
            <div class="icon">M</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(ALERTAS)}</strong>
                <span>alertas em acompanhamento</span>
            </div>
            <div class="icon">A</div>
        </article>
    </section>

    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h1 class="section-title">Painel de cuidado</h1>
            <p class="muted">Acompanhamento centralizado de pacientes, rotinas, servicos e acionamentos criticos.</p>
            <div class="toolbar">
                <button class="danger" onclick="acionarSos()">Acionar SOS</button>
                <a href="/pacientes/rotina/medicamento"><button class="secondary">Nova medicacao</button></a>
            </div>
            <p id="mensagemSos" class="message"></p>
        </article>
        <article class="panel">
            <h2 class="section-title">Paciente em destaque</h2>
            <p><strong>Maria de Lourdes</strong></p>
            <p class="muted">75 anos, monitoramento continuo SOS, rotina de medicamento ativa.</p>
            <span class="status warning">Acompanhamento domiciliar</span>
        </article>
    </section>

    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Rotina de medicamentos</h2>
        <table>
            <thead>
                <tr>
                    <th>Paciente</th>
                    <th>Medicamento</th>
                    <th>Horario</th>
                    <th>Qtd.</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{linhas_medicamentos}</tbody>
        </table>
    </section>

    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Servicos publicados</h2>
        <table>
            <thead>
                <tr>
                    <th>Servico</th>
                    <th>Profissional</th>
                    <th>Valor por turno</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{linhas_servicos}</tbody>
        </table>
    </section>

    <script>
        async function acionarSos() {{
            const mensagem = document.getElementById('mensagemSos');
            mensagem.className = 'message';
            mensagem.innerText = 'Enviando alerta...';
            const resposta = await fetch('/sos', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ paciente: 'Maria de Lourdes', localizacao: 'Residencia' }})
            }});
            const dados = await resposta.json();
            mensagem.className = resposta.ok ? 'message success' : 'message error';
            mensagem.innerText = dados.mensagem;
        }}
    </script>
    """
    return pagina_base("Painel", conteudo)


@app.get("/admin", response_class=HTMLResponse)
def tela_admin():
    linhas_profissionais = "".join(
        f"""
        <tr>
            <td>{item['nome']}</td>
            <td>{item['registro']}</td>
            <td>{item['especialidade']}</td>
            <td>{item['turno']}</td>
            <td><span class="status">{item['status']}</span></td>
        </tr>
        """
        for item in PROFISSIONAIS
    )
    linhas_pacientes = "".join(
        f"""
        <tr>
            <td>{item['nome']}</td>
            <td>{item['idade']}</td>
            <td>{item['cuidador']}</td>
            <td>{item['risco']}</td>
            <td><span class="status warning">{item['status']}</span></td>
        </tr>
        """
        for item in PACIENTES
    )
    conteudo = f"""
    <section class="grid grid-3" aria-label="Resumo administrativo">
        <article class="card metric">
            <div>
                <strong>{len(PACIENTES)}</strong>
                <span>pacientes cadastrados</span>
            </div>
            <div class="icon">P</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(PROFISSIONAIS)}</strong>
                <span>profissionais na rede</span>
            </div>
            <div class="icon">R</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(ALERTAS)}</strong>
                <span>alertas auditaveis</span>
            </div>
            <div class="icon">A</div>
        </article>
    </section>
    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h1 class="section-title">Painel do administrador</h1>
            <p class="muted">Controle de pacientes, profissionais, servicos publicados e indicadores de qualidade.</p>
            <div class="toolbar">
                <a href="/api/profissionais"><button>API profissionais</button></a>
                <a href="/pacientes"><button class="secondary">API pacientes</button></a>
                <a href="/docs"><button class="secondary">Swagger</button></a>
            </div>
        </article>
        <article class="panel">
            <h2 class="section-title">Qualidade do sistema</h2>
            <table>
                <tbody>
                    <tr><th>API</th><td><span class="status">Online</span></td></tr>
                    <tr><th>Testes de API</th><td>pytest validado</td></tr>
                    <tr><th>Testes Web</th><td>Robot Framework validado</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Profissionais cadastrados</h2>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Registro</th>
                    <th>Especialidade</th>
                    <th>Turno</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{linhas_profissionais}</tbody>
        </table>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Pacientes demonstrativos</h2>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Idade</th>
                    <th>Cuidador</th>
                    <th>Risco</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{linhas_pacientes}</tbody>
        </table>
    </section>
    """
    return pagina_base("Admin", conteudo)


@app.get("/profissionais", response_class=HTMLResponse)
@app.get("/profissionais-disponiveis", response_class=HTMLResponse)
def tela_profissionais_disponiveis():
    cards = "".join(
        f"""
        <article class="card professional-card">
            <div class="avatar">{item['nome'][0]}</div>
            <div>
                <h2 class="section-title">{item['nome']}</h2>
                <p class="muted">{item['especialidade']} • {item['cidade']}</p>
            </div>
            <p>{item['resumo']}</p>
            <div>
                <div class="rating">Nota {item['avaliacao']:.1f}/5</div>
                <div class="price">R$ {item['precoTurno']:.2f} por turno</div>
                <p class="muted">{item['turno']} • {item['status']}</p>
            </div>
            <button onclick="selecionarProfissional('{item['nome']}', '{item['especialidade']}')">Selecionar profissional</button>
        </article>
        """
        for item in PROFISSIONAIS
    )
    conteudo = f"""
    <section class="panel">
        <h1 class="section-title">Profissionais disponiveis</h1>
        <p class="muted">Escolha um cuidador, enfermeiro ou fisioterapeuta para simular a contratacao do cuidado domiciliar.</p>
        <p id="profissionalSelecionado" class="message" aria-live="polite"></p>
    </section>
    <section class="marketplace" style="margin-top:16px">
        {cards}
    </section>
    <script>
        function selecionarProfissional(nome, especialidade) {{
            const mensagem = document.getElementById('profissionalSelecionado');
            mensagem.className = 'message success';
            mensagem.innerText = 'Profissional selecionado: ' + nome + ' (' + especialidade + ')';
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
    </script>
    """
    return pagina_base("Profissionais disponiveis", conteudo)


@app.get("/profissional", response_class=HTMLResponse)
def tela_profissional():
    linhas_pacientes = "".join(
        f"""
        <tr>
            <td>{item['nome']}</td>
            <td>{item['idade']}</td>
            <td>{item['necessidadePrincipal']}</td>
            <td><span class="status">Em cuidado</span></td>
        </tr>
        """
        for item in PACIENTES
    )
    conteudo = f"""
    <section class="grid grid-2">
        <article class="panel">
            <h1 class="section-title">Painel do profissional</h1>
            <p class="muted">Rotina operacional do cuidador: medicacoes, pacientes, notificacoes e acionamento de SOS.</p>
            <div class="toolbar">
                <a href="/pacientes/rotina/medicamento"><button>Registrar medicacao</button></a>
                <button class="danger" onclick="acionarSosProfissional()">SOS</button>
            </div>
            <p id="mensagemSosProfissional" class="message"></p>
        </article>
        <article class="panel">
            <h2 class="section-title">Agenda do turno</h2>
            <table>
                <tbody>
                    <tr><th>08:00</th><td>Losartana 50mg</td></tr>
                    <tr><th>10:30</th><td>Hidratacao assistida</td></tr>
                    <tr><th>14:00</th><td>Verificacao de sinais vitais</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Pacientes vinculados</h2>
        <table>
            <thead>
                <tr>
                    <th>Paciente</th>
                    <th>Idade</th>
                    <th>Necessidade principal</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{linhas_pacientes}</tbody>
        </table>
    </section>
    <script>
        async function acionarSosProfissional() {{
            const mensagem = document.getElementById('mensagemSosProfissional');
            mensagem.className = 'message';
            mensagem.innerText = 'Enviando alerta...';
            const resposta = await fetch('/sos', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ paciente: 'Maria de Lourdes', localizacao: 'Residencia' }})
            }});
            const dados = await resposta.json();
            mensagem.className = resposta.ok ? 'message success' : 'message error';
            mensagem.innerText = dados.mensagem;
        }}
    </script>
    """
    return pagina_base("Profissional", conteudo)


@app.get("/paciente", response_class=HTMLResponse)
def tela_paciente():
    linhas_medicamentos = "".join(
        f"""
        <tr>
            <td>{item['nomeRemedio']}</td>
            <td>{item['horarioRemedio']}</td>
            <td>{item['quantidadeRemedio']}</td>
            <td><span class="status">{item['status']}</span></td>
        </tr>
        """
        for item in MEDICAMENTOS
    )
    conteudo = f"""
    <section class="grid grid-2">
        <article class="panel">
            <h1 class="section-title">Painel do paciente</h1>
            <p class="muted">Visao simplificada para acompanhar rotina, lembretes e pedido de ajuda.</p>
            <button class="danger" onclick="acionarSosPaciente()">Pedir ajuda</button>
            <p id="mensagemSosPaciente" class="message"></p>
        </article>
        <article class="panel">
            <h2 class="section-title">Dados do paciente</h2>
            <table>
                <tbody>
                    <tr><th>Nome</th><td>Maria de Lourdes</td></tr>
                    <tr><th>Idade</th><td>75 anos</td></tr>
                    <tr><th>Responsavel</th><td>Responsavel familiar</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Minha rotina de medicamentos</h2>
        <table>
            <thead>
                <tr>
                    <th>Medicamento</th>
                    <th>Horario</th>
                    <th>Qtd.</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{linhas_medicamentos}</tbody>
        </table>
    </section>
    <script>
        async function acionarSosPaciente() {{
            const mensagem = document.getElementById('mensagemSosPaciente');
            mensagem.className = 'message';
            mensagem.innerText = 'Chamando responsaveis...';
            const resposta = await fetch('/sos', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ paciente: 'Maria de Lourdes', localizacao: 'Botao do paciente' }})
            }});
            const dados = await resposta.json();
            mensagem.className = resposta.ok ? 'message success' : 'message error';
            mensagem.innerText = dados.mensagem;
        }}
    </script>
    """
    return pagina_base("Paciente", conteudo)


@app.get("/familiar", response_class=HTMLResponse)
def tela_familiar():
    linhas_alertas = "".join(
        f"""
        <tr>
            <td>{item['tipo']}</td>
            <td>{item.get('mensagem', item.get('descricao', 'Alerta registrado'))}</td>
            <td><span class="status warning">{item['status']}</span></td>
        </tr>
        """
        for item in ALERTAS
    )
    conteudo = f"""
    <section class="grid grid-2">
        <article class="panel">
            <h1 class="section-title">Painel do familiar</h1>
            <p class="muted">Acompanhamento remoto do cuidado, medicamentos, alertas e historico de servicos.</p>
            <div class="toolbar">
                <a href="/paciente"><button>Ver paciente</button></a>
                <a href="/servicos"><button class="secondary">Ver servicos</button></a>
            </div>
        </article>
        <article class="panel">
            <h2 class="section-title">Resumo do cuidado</h2>
            <table>
                <tbody>
                    <tr><th>Paciente</th><td>Maria de Lourdes</td></tr>
                    <tr><th>Cuidador</th><td>Cuidador demonstracao</td></tr>
                    <tr><th>Alertas</th><td>{len(ALERTAS)} registros</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Alertas recentes</h2>
        <table>
            <thead>
                <tr>
                    <th>Tipo</th>
                    <th>Mensagem</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{linhas_alertas}</tbody>
        </table>
    </section>
    """
    return pagina_base("Familiar", conteudo)


@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
def tela_login():
    conteudo = f"""
    <section class="login-layout">
        <div class="login-intro">
            <div class="logo-large">CL+</div>
            <div>
                <h1>Care on Live</h1>
                <p class="muted">Gestao de cuidado domiciliar com pacientes, profissionais, medicamentos e alertas.</p>
            </div>
            <div class="toolbar">
                <a href="/profissionais"><button>Ver profissionais disponiveis</button></a>
                <a href="/pacientes/rotina/medicamento"><button class="secondary">Medicamentos</button></a>
            </div>
        </div>
        <article class="panel login-panel">
            <h1 class="section-title">Login Care on Live</h1>
            <form onsubmit="validarLogin(); return false;">
                <label>Email
                    <input type="text" id="email" placeholder="seu-email@exemplo.com" autocomplete="username" />
                </label>
                <label>Senha
                    <input type="password" id="senha" placeholder="Digite sua senha" autocomplete="current-password" />
                </label>
                <button id="btnEntrar" type="button" onclick="validarLogin()">Entrar</button>
                <div id="toast-mensagem" class="message" aria-live="polite"></div>
                <div id="atalho-dashboard" class="message"></div>
            </form>
            <p class="muted" style="margin-top:16px">Quer contratar alguem? <a href="/profissionais">Ver profissionais disponiveis</a></p>
        </article>
    </section>
    <script>
        async function validarLogin() {{
            var email = document.getElementById('email').value;
            var senha = document.getElementById('senha').value;
            var msg = document.getElementById('toast-mensagem');
            var atalho = document.getElementById('atalho-dashboard');
            msg.className = 'message';
            atalho.innerHTML = '';

            if (!email) {{
                msg.className = 'message error';
                msg.innerText = 'Email obrigat\u00f3rio';
                return;
            }}
            if (!senha) {{
                msg.className = 'message error';
                msg.innerText = 'Senha obrigat\u00f3ria';
                return;
            }}

            const resposta = await fetch('/api/login', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ email: email, senha: senha }})
            }});
            const dados = await resposta.json();

            if (resposta.ok) {{
                msg.className = 'message success';
                msg.innerText = dados.mensagem;
                atalho.innerHTML = '<a href="' + dados.usuario.dashboard + '">Abrir painel ' + dados.usuario.perfil + '</a>';
                return;
            }}

            msg.className = 'message error';
            msg.innerText = dados.mensagem;
        }}
    </script>
    """
    return pagina_base("Login", conteudo)


@app.get("/login-rapido/{perfil}", response_class=HTMLResponse)
def login_rapido(perfil: str):
    usuario_encontrado = next(
        (
            (email, usuario)
            for email, usuario in USUARIOS.items()
            if usuario["perfil"] == perfil
        ),
        None,
    )
    if not usuario_encontrado:
        conteudo = """
        <section class="panel">
            <h1 class="section-title">Perfil nao encontrado</h1>
            <p class="muted">Volte para a tela de login e escolha um dos perfis disponiveis.</p>
            <a href="/login"><button>Voltar</button></a>
        </section>
        """
        return pagina_base("Login rapido", conteudo)

    email, usuario = usuario_encontrado
    conteudo = f"""
    <section class="panel">
        <h1 class="section-title">Login rapido</h1>
        <p class="muted">Perfil autenticado para demonstracao: {usuario['perfil']}.</p>
        <table>
            <tbody>
                <tr><th>Email</th><td>{email}</td></tr>
                <tr><th>Usuario</th><td>{usuario['nome']}</td></tr>
                <tr><th>Tela inicial</th><td>{usuario['dashboard']}</td></tr>
            </tbody>
        </table>
        <div class="toolbar" style="margin-top:16px">
            <a href="{usuario['dashboard']}"><button>Abrir painel</button></a>
            <a href="/login"><button class="secondary">Trocar perfil</button></a>
        </div>
    </section>
    """
    return pagina_base("Login rapido", conteudo)


@app.get("/pacientes/rotina/medicamento", response_class=HTMLResponse)
def tela_medicamento():
    conteudo = """
    <section class="grid grid-2">
        <article class="panel">
            <h1 class="section-title">Cadastro de Medicamento</h1>
            <form onsubmit="validarMedicamento(); return false;">
                <label>Nome do medicamento
                    <input type="text" id="nomeRemedio" placeholder="Losartana 50mg" />
                </label>
                <label>Horario
                    <input type="text" id="horarioRemedio" placeholder="08:00" />
                </label>
                <label>Quantidade
                    <input type="number" id="quantidadeRemedio" placeholder="1" min="0" />
                </label>
                <button id="btnSalvarMedicamento" type="button" onclick="validarMedicamento()">Salvar</button>
                <div id="alertaFormulario" class="message" aria-live="polite"></div>
            </form>
        </article>
        <article class="panel">
            <h2 class="section-title">Regra de qualidade</h2>
            <p class="muted">A rotina so pode ser gravada com nome, horario e quantidade maior que zero.</p>
            <table>
                <tbody>
                    <tr><th>Paciente</th><td>Maria de Lourdes</td></tr>
                    <tr><th>Status</th><td><span class="status">Rotina ativa</span></td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <script>
        async function validarMedicamento() {
            var nome = document.getElementById('nomeRemedio').value;
            var horario = document.getElementById('horarioRemedio').value;
            var qtd = document.getElementById('quantidadeRemedio').value;
            var msg = document.getElementById('alertaFormulario');
            msg.className = 'message';

            if (!nome) {
                msg.className = 'message error';
                msg.innerText = 'Nome do medicamento obrigat\u00f3rio';
                return;
            }
            if (!horario) {
                msg.className = 'message error';
                msg.innerText = 'Hor\u00e1rio obrigat\u00f3rio';
                return;
            }
            if (Number(qtd) <= 0) {
                msg.className = 'message error';
                msg.innerText = 'A quantidade deve ser maior que zero';
                return;
            }

            msg.className = 'message success';
            msg.innerText = 'Medica\u00e7\u00e3o salva na rotina';
            fetch('/medicamentos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    paciente: 'Maria de Lourdes',
                    nomeRemedio: nome,
                    horarioRemedio: horario,
                    quantidadeRemedio: Number(qtd)
                })
            });
        }
    </script>
    """
    return pagina_base("Medicamentos", conteudo)
