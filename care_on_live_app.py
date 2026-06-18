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


class CadastroUsuario(BaseModel):
    nome: str = Field(min_length=1)
    email: str = Field(min_length=1)
    senha: str = Field(min_length=1)
    perfil: str = "familiar"


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
        "email": "ana.ribeiro@careonlive.example",
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
        "email": "bruno.costa@careonlive.example",
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
        "email": "camila.nascimento@careonlive.example",
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
        "email": "diego.rocha@careonlive.example",
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
        "status": "Tomado",
        "tomou": True,
        "horaTomada": "08:07",
    },
    {
        "idMedicamento": "m002",
        "paciente": "Jose Carlos Pereira",
        "nomeRemedio": "Metformina 850mg",
        "horarioRemedio": "12:00",
        "quantidadeRemedio": 1,
        "status": "Agendado",
        "tomou": False,
        "horaTomada": "",
    },
    {
        "idMedicamento": "m003",
        "paciente": "Helena Duarte Lima",
        "nomeRemedio": "Vitamina D",
        "horarioRemedio": "09:30",
        "quantidadeRemedio": 1,
        "status": "Tomado",
        "tomou": True,
        "horaTomada": "09:36",
    },
    {
        "idMedicamento": "m004",
        "paciente": "Antonio Silva Ramos",
        "nomeRemedio": "Anticoagulante",
        "horarioRemedio": "20:00",
        "quantidadeRemedio": 1,
        "status": "Pendente",
        "tomou": False,
        "horaTomada": "",
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

DASHBOARDS_POR_PERFIL = {
    "administrador": "/admin",
    "profissional": "/profissional",
    "paciente": "/paciente",
    "familiar": "/familiar",
}

PERFIS_CADASTRO_PUBLICO = {"profissional", "paciente", "familiar"}


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
            .modal-backdrop {{
                position: fixed;
                inset: 0;
                background: rgba(23, 33, 38, 0.58);
                display: none;
                align-items: center;
                justify-content: center;
                padding: 18px;
                z-index: 20;
            }}
            .modal-backdrop.aberto {{
                display: flex;
            }}
            .modal {{
                width: min(420px, 100%);
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 18px;
            }}
            [hidden] {{
                display: none !important;
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
            button, .button-link {{
                min-height: 42px;
                border: 0;
                border-radius: 8px;
                padding: 10px 14px;
                background: var(--primary);
                color: #fff;
                font-weight: 700;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
            }}
            button:hover, .button-link:hover {{
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
            .demo-access {{
                margin-top: 16px;
                display: grid;
                gap: 10px;
            }}
            .demo-access h2 {{
                margin: 0;
                font-size: 16px;
            }}
            .demo-access-list {{
                display: grid;
                gap: 8px;
            }}
            .demo-access-item {{
                display: grid;
                grid-template-columns: minmax(0, 1fr) auto;
                gap: 10px;
                align-items: center;
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 10px;
                background: var(--surface-soft);
            }}
            .demo-access-item strong {{
                display: block;
                margin-bottom: 4px;
            }}
            .demo-access-item span {{
                display: block;
                color: var(--muted);
                font-size: 12px;
                overflow-wrap: anywhere;
            }}
            .demo-access-item button {{
                min-width: 74px;
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
                .demo-access-item {{
                    grid-template-columns: 1fr;
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
                    <a id="navHome" href="/">Home</a>
                    <a id="navProfissionais" href="/profissionais">Profissionais disponiveis</a>
                    <a class="nav-publico" href="/login">Login</a>
                    <a class="nav-publico" href="/cadastro">Cadastro</a>
                    <a id="navMeuPainel" href="#" hidden>Meu painel</a>
                    <a id="navMedicamentos" href="/pacientes/rotina/medicamento">Medicamentos</a>
                    <a id="navSair" href="/login" hidden>Sair</a>
                </nav>
            </div>
        </header>
        <main>{conteudo}</main>
        <script>
            (function () {{
                function usuarioLogado() {{
                    try {{
                        return JSON.parse(localStorage.getItem('careOnLiveUsuario'));
                    }} catch (erro) {{
                        return null;
                    }}
                }}

                var usuario = usuarioLogado();
                var linksPublicos = document.querySelectorAll('.nav-publico');
                var linkPainel = document.getElementById('navMeuPainel');
                var linkSair = document.getElementById('navSair');
                var linkProfissionais = document.getElementById('navProfissionais');
                var linkMedicamentos = document.getElementById('navMedicamentos');
                var linkHome = document.getElementById('navHome');

                if (usuario && usuario.dashboard) {{
                    linksPublicos.forEach(function (link) {{
                        link.hidden = true;
                    }});
                    linkPainel.hidden = false;
                    linkPainel.href = usuario.dashboard;
                    linkSair.hidden = false;
                    if (linkHome) {{
                        linkHome.href = usuario.dashboard;
                    }}
                    if (usuario.perfil === 'profissional' && linkProfissionais) {{
                        linkProfissionais.hidden = true;
                    }}
                    if (usuario.perfil === 'profissional' && linkMedicamentos) {{
                        linkMedicamentos.hidden = true;
                    }}
                }}

                if (linkSair) {{
                    linkSair.addEventListener('click', function () {{
                        localStorage.removeItem('careOnLiveUsuario');
                    }});
                }}
            }})();
        </script>
    </body>
    </html>
    """


def script_redirecionar_usuario_logado() -> str:
    return """
    <script>
        (function () {
            try {
                var usuario = JSON.parse(localStorage.getItem('careOnLiveUsuario'));
                if (usuario && usuario.dashboard) {
                    window.location.href = usuario.dashboard;
                }
            } catch (erro) {}
        })();
    </script>
    """


def script_exigir_perfil(perfil_esperado: str) -> str:
    return f"""
    <script>
        (function () {{
            var usuario = null;
            try {{
                usuario = JSON.parse(localStorage.getItem('careOnLiveUsuario'));
            }} catch (erro) {{}}

            if (!usuario || !usuario.perfil) {{
                window.location.href = '/login';
                return;
            }}

            if (usuario.perfil !== '{perfil_esperado}') {{
                window.location.href = usuario.dashboard || '/login';
            }}
        }})();
    </script>
    """


def tabela_medicamentos_paciente(paciente: Optional[str] = None, mostrar_acao: bool = True) -> str:
    medicamentos = [
        item
        for item in MEDICAMENTOS
        if paciente is None or item["paciente"] == paciente
    ]
    linhas = ""
    for item in medicamentos:
        status_tomou = "Sim" if item.get("tomou") else "Nao"
        classe_status = "status" if item.get("tomou") else "status warning"
        hora_tomada = item.get("horaTomada") or "Aguardando"
        acao = ""
        if mostrar_acao:
            acao = (
                f"<button type=\"button\" onclick=\"abrirModalTomada("
                f"'{item['idMedicamento']}', '{item['nomeRemedio']}')\">Registrar tomada</button>"
            )
        linhas += f"""
        <tr>
            <td>{item['paciente']}</td>
            <td>{item['nomeRemedio']}</td>
            <td>{item['horarioRemedio']}</td>
            <td>{item['quantidadeRemedio']}</td>
            <td><span class="{classe_status}">{status_tomou}</span></td>
            <td>{hora_tomada}</td>
            <td>{item['status']}</td>
            <td>{acao}</td>
        </tr>
        """
    return f"""
    <table>
        <thead>
            <tr>
                <th>Paciente</th>
                <th>Medicamento</th>
                <th>Horario previsto</th>
                <th>Qtd.</th>
                <th>Tomou?</th>
                <th>Hora registrada</th>
                <th>Status</th>
                <th>Acao</th>
            </tr>
        </thead>
        <tbody>{linhas}</tbody>
    </table>
    """


def modal_registrar_tomada() -> str:
    return """
<div id="modalTomada" class="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="tituloModalTomada">
    <article class="modal">
        <h2 id="tituloModalTomada" class="section-title">Registrar tomada</h2>
        <p id="remedioModalTomada" class="muted">Selecione a hora em que o medicamento foi tomado.</p>
        <label>Hora da tomada
            <input type="time" id="horaTomadaModal" />
        </label>
        <div class="toolbar" style="margin-top:14px">
            <button type="button" onclick="confirmarTomadaModal()">Confirmar</button>
            <button type="button" class="secondary" onclick="fecharModalTomada()">Cancelar</button>
        </div>
    </article>
</div>
<script>
    var tomadaAtual = { id: '', remedio: '', linha: null, botao: null };

    function abrirModalTomada(id, remedio) {
        tomadaAtual.id = id;
        tomadaAtual.remedio = remedio;
        tomadaAtual.botao = event.target;
        tomadaAtual.linha = tomadaAtual.botao.closest('tr');
        document.getElementById('remedioModalTomada').innerText = remedio;
        document.getElementById('horaTomadaModal').value = '';
        document.getElementById('modalTomada').classList.add('aberto');
        document.getElementById('horaTomadaModal').focus();
    }

    function fecharModalTomada() {
        document.getElementById('modalTomada').classList.remove('aberto');
    }

    function confirmarTomadaModal() {
        const hora = document.getElementById('horaTomadaModal').value;
        if (!hora) {
            const mensagem = document.getElementById('mensagemMedicamentos') || document.getElementById('mensagemFamiliar') || document.getElementById('mensagemSosPaciente');
            if (mensagem) {
                mensagem.className = 'message error';
                mensagem.innerText = 'Selecione a hora da tomada.';
            }
            return;
        }
        const linha = tomadaAtual.linha;
        const botao = tomadaAtual.botao;
        linha.children[4].innerHTML = '<span class="status">Sim</span>';
        linha.children[5].innerText = hora;
        linha.children[6].innerText = 'Tomado';
        botao.disabled = true;
        botao.innerText = 'Registrado';
        const mensagem = document.getElementById('mensagemMedicamentos') || document.getElementById('mensagemFamiliar') || document.getElementById('mensagemSosPaciente');
        if (mensagem) {
            mensagem.className = 'message success';
            mensagem.innerText = tomadaAtual.remedio + ' registrado como tomado as ' + hora + '.';
        }
        fecharModalTomada();
    }
</script>
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
                "email": credenciais.email,
                "perfil": usuario["perfil"],
                "dashboard": usuario["dashboard"],
            },
        }
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"status": "erro", "mensagem": "Credenciais inv\u00e1lidas"}


@app.post("/api/cadastro")
def cadastrar_usuario(cadastro: CadastroUsuario, response: Response):
    email = cadastro.email.strip().lower()
    nome = cadastro.nome.strip()
    senha = cadastro.senha.strip()
    perfil = cadastro.perfil.strip().lower()

    if not nome:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "Nome obrigat\u00f3rio"}
    if not email:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "Email obrigat\u00f3rio"}
    if "@" not in email:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "Email inv\u00e1lido"}
    if not senha:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "Senha obrigat\u00f3ria"}
    if len(senha) < 6:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "Senha deve ter pelo menos 6 caracteres"}
    if perfil not in PERFIS_CADASTRO_PUBLICO:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "erro", "mensagem": "Perfil inv\u00e1lido"}
    if email in USUARIOS:
        response.status_code = status.HTTP_409_CONFLICT
        return {"status": "erro", "mensagem": "Email j\u00e1 cadastrado"}

    USUARIOS[email] = {
        "senha": senha,
        "perfil": perfil,
        "nome": nome,
        "dashboard": DASHBOARDS_POR_PERFIL[perfil],
    }

    response.status_code = status.HTTP_201_CREATED
    return {
        "status": "sucesso",
        "mensagem": "Cadastro realizado com sucesso",
        "usuario": {
            "nome": nome,
            "email": email,
            "perfil": perfil,
            "dashboard": DASHBOARDS_POR_PERFIL[perfil],
        },
    }


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
    linhas_usuarios = "".join(
        f"""
        <tr>
            <td>{usuario['nome']}</td>
            <td>{email}</td>
            <td>{usuario['perfil']}</td>
            <td>{usuario['dashboard']}</td>
            <td><span class="status">Ativo</span></td>
        </tr>
        """
        for email, usuario in USUARIOS.items()
    )
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
    linhas_alertas = "".join(
        f"""
        <tr>
            <td>{item['tipo']}</td>
            <td>{item.get('paciente', '-')}</td>
            <td>{item.get('mensagem', item.get('descricao', 'Alerta registrado'))}</td>
            <td><span class="status warning">{item['status']}</span></td>
            <td><button type="button" onclick="resolverAlertaAdmin(this)">Resolver</button></td>
        </tr>
        """
        for item in ALERTAS
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
    <section class="grid grid-3" style="margin-top:16px" aria-label="Resumo de operacao">
        <article class="card metric">
            <div>
                <strong>{len(USUARIOS)}</strong>
                <span>usuarios do sistema</span>
            </div>
            <div class="icon">U</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(SERVICOS)}</strong>
                <span>servicos publicados</span>
            </div>
            <div class="icon">S</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(MEDICAMENTOS)}</strong>
                <span>medicamentos registrados</span>
            </div>
            <div class="icon">M</div>
        </article>
    </section>
    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h1 class="section-title">Painel do administrador</h1>
            <p class="muted">Visualizacao completa do sistema: usuarios, pacientes, profissionais, servicos, medicamentos, alertas e qualidade operacional.</p>
            <div class="toolbar">
                <a href="/api/profissionais"><button>API profissionais</button></a>
                <a href="/pacientes"><button class="secondary">API pacientes</button></a>
                <a href="/docs"><button class="secondary">Swagger</button></a>
                <button type="button" onclick="gerarRelatorioAdmin()">Gerar relatorio</button>
            </div>
            <p id="mensagemAdmin" class="message"></p>
        </article>
        <article class="panel">
            <h2 class="section-title">Qualidade do sistema</h2>
            <table>
                <tbody>
                    <tr><th>API</th><td><span class="status">Online</span></td></tr>
                    <tr><th>Testes de API</th><td>pytest validado</td></tr>
                    <tr><th>Testes Web</th><td>Robot Framework validado</td></tr>
                    <tr><th>Perfis</th><td>Administrador, profissional, paciente e familiar</td></tr>
                    <tr><th>Cadastro publico</th><td>Paciente, familiar e profissional</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Usuarios cadastrados</h2>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Email</th>
                    <th>Perfil</th>
                    <th>Painel</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{linhas_usuarios}</tbody>
        </table>
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
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Medicamentos registrados</h2>
        {tabela_medicamentos_paciente(None, mostrar_acao=False)}
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Alertas e ocorrencias</h2>
        <table>
            <thead>
                <tr>
                    <th>Tipo</th>
                    <th>Paciente</th>
                    <th>Descricao</th>
                    <th>Status</th>
                    <th>Acao</th>
                </tr>
            </thead>
            <tbody>{linhas_alertas}</tbody>
        </table>
    </section>
    <script>
        function gerarRelatorioAdmin() {{
            const mensagem = document.getElementById('mensagemAdmin');
            mensagem.className = 'message success';
            mensagem.innerText = 'Relatorio administrativo gerado para conferencia.';
        }}
        function resolverAlertaAdmin(botao) {{
            const linha = botao.closest('tr');
            linha.children[3].innerHTML = '<span class="status">Resolvido</span>';
            botao.disabled = true;
            botao.innerText = 'Resolvido';
            const mensagem = document.getElementById('mensagemAdmin');
            mensagem.className = 'message success';
            mensagem.innerText = 'Alerta marcado como resolvido.';
        }}
    </script>
    """
    return pagina_base("Admin", conteudo + script_exigir_perfil("administrador"))


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
            <a class="button-link" href="mailto:{item['email']}?subject=Interesse%20em%20atendimento%20Care%20on%20Live">Selecionar profissional</a>
        </article>
        """
        for item in PROFISSIONAIS
    )
    conteudo = f"""
    <section class="panel">
        <h1 class="section-title">Profissionais disponiveis</h1>
        <p class="muted">Escolha um cuidador, enfermeiro ou fisioterapeuta para simular a contratacao do cuidado domiciliar.</p>
    </section>
    <section class="marketplace" style="margin-top:16px">
        {cards}
    </section>
    """
    return pagina_base("Profissionais disponiveis", conteudo)


@app.get("/profissional", response_class=HTMLResponse)
def tela_profissional():
    solicitacoes_servico = [
        {
            "id": "sol001",
            "solicitante": "Responsavel familiar",
            "paciente": "Maria de Lourdes",
            "servico": "Cuidador noturno",
            "periodo": "Segunda a sexta",
        },
        {
            "id": "sol002",
            "solicitante": "Familia Pereira",
            "paciente": "Jose Carlos Pereira",
            "servico": "Afericao de pressao e glicemia",
            "periodo": "Manha",
        },
        {
            "id": "sol003",
            "solicitante": "Familia Duarte",
            "paciente": "Helena Duarte Lima",
            "servico": "Fisioterapia domiciliar",
            "periodo": "Terca e quinta",
        },
    ]
    pacientes_profissional = [
        {
            "nome": "Maria de Lourdes",
            "idade": 75,
            "necessidade": "Controle de medicacao e acompanhamento noturno",
            "familiar": "Responsavel familiar",
            "status": "Em acompanhamento",
        },
        {
            "nome": "Jose Carlos Pereira",
            "idade": 82,
            "necessidade": "Glicemia e pressao arterial",
            "familiar": "Familia Pereira",
            "status": "Rotina ativa",
        },
        {
            "nome": "Helena Duarte Lima",
            "idade": 69,
            "necessidade": "Fisioterapia e prevencao de quedas",
            "familiar": "Familia Duarte",
            "status": "Em acompanhamento",
        },
    ]
    linhas_solicitacoes_servico = "".join(
        f"""
        <tr id="{item['id']}">
            <td>{item['solicitante']}</td>
            <td>{item['paciente']}</td>
            <td>{item['servico']}</td>
            <td>{item['periodo']}</td>
            <td><span class="status warning" id="{item['id']}-status">Pendente</span></td>
            <td>
                <div class="toolbar">
                    <button type="button" onclick="decidirSolicitacao('{item['id']}', '{item['paciente']}', 'aceita')">Aceitar</button>
                    <button type="button" class="danger" onclick="decidirSolicitacao('{item['id']}', '{item['paciente']}', 'recusada')">Recusar</button>
                </div>
            </td>
        </tr>
        """
        for item in solicitacoes_servico
    )
    linhas_pacientes = "".join(
        f"""
        <tr>
            <td>{item['nome']}</td>
            <td>{item['idade']}</td>
            <td>{item['necessidade']}</td>
            <td>{item['familiar']}</td>
            <td><span class="status">{item['status']}</span></td>
            <td>
                <div class="toolbar">
                    <button type="button" onclick="selecionarPaciente('{item['nome']}', '{item['familiar']}')">Selecionar</button>
                    <button type="button" class="secondary" onclick="prepararRemedio('{item['nome']}')">Passar remedio</button>
                </div>
            </td>
        </tr>
        """
        for item in pacientes_profissional
    )
    conteudo = f"""
    <section class="grid grid-3" aria-label="Indicadores do profissional">
        <article class="card metric">
            <div>
                <strong>{len(solicitacoes_servico)}</strong>
                <span>solicitacoes de servico</span>
            </div>
            <div class="icon">P</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(pacientes_profissional)}</strong>
                <span>pacientes vinculados</span>
            </div>
            <div class="icon">P</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(pacientes_profissional)}</strong>
                <span>familias para contato</span>
            </div>
            <div class="icon">F</div>
        </article>
    </section>
    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h1 class="section-title">Painel do profissional</h1>
            <p class="muted">Tela de trabalho do profissional para acompanhar seus pacientes, prescrever remedios e conversar com paciente ou familia.</p>
            <div class="toolbar">
                <button class="secondary" onclick="registrarSinaisVitais()">Registrar sinais vitais</button>
                <button class="danger" onclick="acionarSosProfissional()">SOS</button>
            </div>
            <p id="mensagemProfissional" class="message"></p>
        </article>
        <article class="panel">
            <h2 class="section-title">Agenda do turno</h2>
            <table>
                <tbody>
                    <tr><th>08:00</th><td>Administrar Losartana 50mg</td><td><button type="button" onclick="concluirTarefa('Medicacao das 08:00')">Concluir</button></td></tr>
                    <tr><th>10:30</th><td>Hidratacao assistida</td><td><button type="button" onclick="concluirTarefa('Hidratacao assistida')">Concluir</button></td></tr>
                    <tr><th>14:00</th><td>Verificacao de sinais vitais</td><td><button type="button" onclick="concluirTarefa('Sinais vitais')">Concluir</button></td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Solicitacoes de servico</h2>
        <table>
            <thead>
                <tr>
                    <th>Solicitante</th>
                    <th>Paciente</th>
                    <th>Servico</th>
                    <th>Periodo</th>
                    <th>Status</th>
                    <th>Decisao</th>
                </tr>
            </thead>
            <tbody>{linhas_solicitacoes_servico}</tbody>
        </table>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Meus pacientes</h2>
        <table>
            <thead>
                <tr>
                    <th>Paciente</th>
                    <th>Idade</th>
                    <th>Necessidade</th>
                    <th>Familiar</th>
                    <th>Status</th>
                    <th>Acao</th>
                </tr>
            </thead>
            <tbody>{linhas_pacientes}</tbody>
        </table>
    </section>
    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h2 class="section-title">Passar remedio para paciente</h2>
            <form onsubmit="passarRemedioPaciente(); return false;">
                <label>Paciente
                    <input type="text" id="pacienteSelecionado" value="Maria de Lourdes" />
                </label>
                <label>Remedio
                    <input type="text" id="remedioProfissional" placeholder="Ex: Losartana 50mg" />
                </label>
                <label>Horario
                    <input type="text" id="horarioProfissional" placeholder="Ex: 08:00" />
                </label>
                <label>Quantidade
                    <input type="number" id="quantidadeProfissional" min="1" value="1" />
                </label>
                <button type="button" onclick="passarRemedioPaciente()">Salvar remedio</button>
            </form>
        </article>
        <article class="panel">
            <h2 class="section-title">Conversa com paciente</h2>
            <table>
                <tbody id="conversaPaciente">
                    <tr><th>Maria de Lourdes</th><td>Preciso confirmar o horario do remedio de hoje.</td></tr>
                    <tr><th>Profissional</th><td>Vou acompanhar sua rotina e retorno ainda hoje.</td></tr>
                </tbody>
            </table>
            <form onsubmit="enviarMensagemProfissional(); return false;" style="margin-top:12px">
                <label>Mensagem ao paciente
                    <textarea id="mensagemProfissionalPaciente" placeholder="Escreva uma resposta para o paciente"></textarea>
                </label>
                <button type="button" onclick="enviarMensagemProfissional()">Enviar mensagem</button>
            </form>
        </article>
    </section>
    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h2 class="section-title">Mensagem para familia</h2>
            <form onsubmit="enviarMensagemFamiliaProfissional(); return false;">
                <label>Familiar
                    <input type="text" id="familiarSelecionado" value="Responsavel familiar" />
                </label>
                <label>Mensagem
                    <textarea id="mensagemProfissionalFamilia" placeholder="Escreva uma orientacao para a familia"></textarea>
                </label>
                <button type="button" onclick="enviarMensagemFamiliaProfissional()">Enviar para familia</button>
            </form>
        </article>
        <article class="panel">
            <h2 class="section-title">Registro de evolucao</h2>
            <form onsubmit="salvarEvolucao(); return false;">
                <label>Anotacao do atendimento
                    <textarea id="evolucaoProfissional" placeholder="Ex: paciente orientado, medicacao administrada, sinais estaveis"></textarea>
                </label>
                <button type="button" onclick="salvarEvolucao()">Salvar evolucao</button>
            </form>
        </article>
    </section>
    <script>
        async function acionarSosProfissional() {{
            const mensagem = document.getElementById('mensagemProfissional');
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
        function registrarSinaisVitais() {{
            const mensagem = document.getElementById('mensagemProfissional');
            mensagem.className = 'message success';
            mensagem.innerText = 'Sinais vitais registrados para acompanhamento.';
        }}
        function decidirSolicitacao(id, paciente, decisao) {{
            const status = document.getElementById(id + '-status');
            const mensagem = document.getElementById('mensagemProfissional');
            status.className = decisao === 'aceita' ? 'status' : 'status warning';
            status.innerText = decisao === 'aceita' ? 'Aceita' : 'Recusada';
            mensagem.className = decisao === 'aceita' ? 'message success' : 'message';
            mensagem.innerText = 'Solicitacao de ' + paciente + ' ' + decisao + '.';
        }}
        function selecionarPaciente(paciente, familiar) {{
            const mensagem = document.getElementById('mensagemProfissional');
            document.getElementById('pacienteSelecionado').value = paciente;
            document.getElementById('familiarSelecionado').value = familiar;
            mensagem.className = 'message success';
            mensagem.innerText = paciente + ' selecionado para atendimento.';
        }}
        function prepararRemedio(paciente) {{
            document.getElementById('pacienteSelecionado').value = paciente;
            document.getElementById('remedioProfissional').focus();
        }}
        function concluirTarefa(tarefa) {{
            const mensagem = document.getElementById('mensagemProfissional');
            mensagem.className = 'message success';
            mensagem.innerText = tarefa + ' concluida no turno.';
        }}
        function salvarEvolucao() {{
            const texto = document.getElementById('evolucaoProfissional').value;
            const mensagem = document.getElementById('mensagemProfissional');
            if (!texto) {{
                mensagem.className = 'message error';
                mensagem.innerText = 'Informe a anotacao do atendimento.';
                return;
            }}
            mensagem.className = 'message success';
            mensagem.innerText = 'Evolucao salva no prontuario demonstrativo.';
            document.getElementById('evolucaoProfissional').value = '';
        }}
        function enviarMensagemProfissional() {{
            const campo = document.getElementById('mensagemProfissionalPaciente');
            const conversa = document.getElementById('conversaPaciente');
            const mensagem = document.getElementById('mensagemProfissional');
            if (!campo.value) {{
                mensagem.className = 'message error';
                mensagem.innerText = 'Escreva uma mensagem para o paciente.';
                return;
            }}
            conversa.innerHTML += '<tr><th>Profissional</th><td>' + campo.value + '</td></tr>';
            mensagem.className = 'message success';
            mensagem.innerText = 'Mensagem enviada ao paciente.';
            campo.value = '';
        }}
        function passarRemedioPaciente() {{
            const paciente = document.getElementById('pacienteSelecionado').value;
            const remedio = document.getElementById('remedioProfissional').value;
            const horario = document.getElementById('horarioProfissional').value;
            const quantidade = document.getElementById('quantidadeProfissional').value;
            const mensagem = document.getElementById('mensagemProfissional');
            if (!paciente || !remedio || !horario || Number(quantidade) <= 0) {{
                mensagem.className = 'message error';
                mensagem.innerText = 'Informe paciente, remedio, horario e quantidade.';
                return;
            }}
            mensagem.className = 'message success';
            mensagem.innerText = remedio + ' prescrito para ' + paciente + ' as ' + horario + '.';
            document.getElementById('remedioProfissional').value = '';
            document.getElementById('horarioProfissional').value = '';
            document.getElementById('quantidadeProfissional').value = '1';
        }}
        function enviarMensagemFamiliaProfissional() {{
            const familiar = document.getElementById('familiarSelecionado').value;
            const campo = document.getElementById('mensagemProfissionalFamilia');
            const mensagem = document.getElementById('mensagemProfissional');
            if (!familiar || !campo.value) {{
                mensagem.className = 'message error';
                mensagem.innerText = 'Informe a mensagem para a familia.';
                return;
            }}
            mensagem.className = 'message success';
            mensagem.innerText = 'Mensagem enviada para ' + familiar + '.';
            campo.value = '';
        }}
    </script>
    """
    return pagina_base("Profissional", conteudo + script_exigir_perfil("profissional"))


@app.get("/paciente", response_class=HTMLResponse)
def tela_paciente():
    conteudo = f"""
    <section class="grid grid-3" aria-label="Resumo do paciente">
        <article class="card metric">
            <div>
                <strong>{len([item for item in MEDICAMENTOS if item['paciente'] == 'Maria de Lourdes'])}</strong>
                <span>medicamentos da rotina</span>
            </div>
            <div class="icon">M</div>
        </article>
        <article class="card metric">
            <div>
                <strong>1</strong>
                <span>cuidador responsavel</span>
            </div>
            <div class="icon">C</div>
        </article>
        <article class="card metric">
            <div>
                <strong>24h</strong>
                <span>canal de emergencia</span>
            </div>
            <div class="icon">S</div>
        </article>
    </section>
    <section class="grid grid-2">
        <article class="panel">
            <h1 class="section-title">Painel do paciente</h1>
            <p class="muted">Acompanhe sua rotina, registre remedios tomados, fale com o cuidador e acione ajuda rapidamente.</p>
            <div class="toolbar">
                <button class="danger" onclick="acionarSosPaciente()">Pedir ajuda</button>
                <button class="secondary" onclick="avisarBemEstar()">Estou bem</button>
                <button onclick="solicitarCuidador()">Chamar cuidador</button>
            </div>
            <p id="mensagemSosPaciente" class="message"></p>
        </article>
        <article class="panel">
            <h2 class="section-title">Dados do usuario</h2>
            <table>
                <tbody>
                    <tr><th>Nome</th><td id="dadosPacienteUsuarioNome">Maria de Lourdes</td></tr>
                    <tr><th>Perfil</th><td id="dadosPacienteUsuarioPerfil">paciente</td></tr>
                    <tr><th>Email</th><td id="dadosPacienteUsuarioEmail">paciente@careonlive.com</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h2 class="section-title">Dados de cuidado</h2>
            <table>
                <tbody>
                    <tr><th>Nome</th><td>Maria de Lourdes</td></tr>
                    <tr><th>Idade</th><td>75 anos</td></tr>
                    <tr><th>Responsavel</th><td>Responsavel familiar</td></tr>
                    <tr><th>Profissional</th><td>Cuidador demonstracao</td></tr>
                    <tr><th>Status</th><td><span class="status">Rotina ativa</span></td></tr>
                </tbody>
            </table>
        </article>
        <article class="panel">
            <h2 class="section-title">Contatos de apoio</h2>
            <table>
                <tbody>
                    <tr><th>Familiar principal</th><td>Responsavel familiar - (61) 99999-0101</td></tr>
                    <tr><th>Cuidador</th><td>Cuidador demonstracao - (61) 99999-0404</td></tr>
                    <tr><th>Emergencia</th><td>Canal SOS 24h</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Meus medicamentos</h2>
        <p class="muted">Registre a hora em que tomou cada remedio para familiar e cuidador acompanharem.</p>
        <p id="mensagemMedicamentos" class="message"></p>
        {tabela_medicamentos_paciente("Maria de Lourdes")}
    </section>
    <section class="grid grid-3" style="margin-top:16px">
        <article class="panel">
            <h2 class="section-title">Rotina de hoje</h2>
            <table>
                <tbody>
                    <tr><th>08:00</th><td>Remedio da manha</td><td><button type="button" onclick="registrarRotinaPaciente('Remedio da manha')">Feito</button></td></tr>
                    <tr><th>10:30</th><td>Beber agua</td><td><button type="button" onclick="registrarRotinaPaciente('Hidratacao')">Feito</button></td></tr>
                    <tr><th>16:00</th><td>Caminhada assistida</td><td><button type="button" onclick="registrarRotinaPaciente('Caminhada assistida')">Feito</button></td></tr>
                </tbody>
            </table>
        </article>
        <article class="panel">
            <h2 class="section-title">Mensagem para o cuidador</h2>
            <form onsubmit="enviarMensagemPaciente(); return false;">
                <label>Como voce esta?
                    <textarea id="mensagemPaciente" placeholder="Ex: estou com dor, preciso de ajuda, tomei o remedio"></textarea>
                </label>
                <button type="button" onclick="enviarMensagemPaciente()">Enviar ao cuidador</button>
            </form>
        </article>
        <article class="panel">
            <h2 class="section-title">Mensagem para familia</h2>
            <form onsubmit="enviarMensagemFamiliaPaciente(); return false;">
                <label>Recado para familiar
                    <textarea id="mensagemPacienteFamilia" placeholder="Ex: estou bem, pode ficar tranquilo"></textarea>
                </label>
                <button type="button" onclick="enviarMensagemFamiliaPaciente()">Enviar a familia</button>
            </form>
        </article>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Historico rapido</h2>
        <table>
            <tbody id="historicoPaciente">
                <tr><th>Hoje 08:07</th><td>Losartana 50mg registrada como tomada.</td></tr>
                <tr><th>Hoje 09:00</th><td>Paciente informou bem-estar.</td></tr>
            </tbody>
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
        function avisarBemEstar() {{
            const mensagem = document.getElementById('mensagemSosPaciente');
            mensagem.className = 'message success';
            mensagem.innerText = 'Aviso enviado: paciente informou que esta bem.';
            adicionarHistoricoPaciente('Agora', 'Paciente informou que esta bem.');
        }}
        function solicitarCuidador() {{
            const mensagem = document.getElementById('mensagemSosPaciente');
            mensagem.className = 'message success';
            mensagem.innerText = 'Cuidador notificado para entrar em contato.';
            adicionarHistoricoPaciente('Agora', 'Cuidador chamado pelo paciente.');
        }}
        function registrarRotinaPaciente(item) {{
            const mensagem = document.getElementById('mensagemSosPaciente');
            mensagem.className = 'message success';
            mensagem.innerText = item + ' registrado na rotina.';
            adicionarHistoricoPaciente('Agora', item + ' concluido.');
        }}
        function enviarMensagemPaciente() {{
            const texto = document.getElementById('mensagemPaciente').value;
            const mensagem = document.getElementById('mensagemSosPaciente');
            if (!texto) {{
                mensagem.className = 'message error';
                mensagem.innerText = 'Escreva uma mensagem para o cuidador.';
                return;
            }}
            mensagem.className = 'message success';
            mensagem.innerText = 'Mensagem enviada ao cuidador.';
            adicionarHistoricoPaciente('Agora', 'Mensagem enviada ao cuidador.');
            document.getElementById('mensagemPaciente').value = '';
        }}
        function enviarMensagemFamiliaPaciente() {{
            const texto = document.getElementById('mensagemPacienteFamilia').value;
            const mensagem = document.getElementById('mensagemSosPaciente');
            if (!texto) {{
                mensagem.className = 'message error';
                mensagem.innerText = 'Escreva uma mensagem para a familia.';
                return;
            }}
            mensagem.className = 'message success';
            mensagem.innerText = 'Mensagem enviada a familia.';
            adicionarHistoricoPaciente('Agora', 'Mensagem enviada a familia.');
            document.getElementById('mensagemPacienteFamilia').value = '';
        }}
        function adicionarHistoricoPaciente(hora, texto) {{
            const historico = document.getElementById('historicoPaciente');
            historico.innerHTML = '<tr><th>' + hora + '</th><td>' + texto + '</td></tr>' + historico.innerHTML;
        }}
        (function preencherDadosPacienteUsuario() {{
            try {{
                const usuario = JSON.parse(localStorage.getItem('careOnLiveUsuario'));
                if (!usuario) {{
                    return;
                }}
                document.getElementById('dadosPacienteUsuarioNome').innerText = usuario.nome || 'Maria de Lourdes';
                document.getElementById('dadosPacienteUsuarioPerfil').innerText = usuario.perfil || 'paciente';
                document.getElementById('dadosPacienteUsuarioEmail').innerText = usuario.email || 'Email nao informado';
            }} catch (erro) {{}}
        }})();
    </script>
    """
    return pagina_base("Paciente", conteudo + modal_registrar_tomada() + script_exigir_perfil("paciente"))


@app.get("/familiar", response_class=HTMLResponse)
def tela_familiar():
    linhas_alertas = "".join(
        f"""
        <tr>
            <td>{item['tipo']}</td>
            <td>{item.get('mensagem', item.get('descricao', 'Alerta registrado'))}</td>
            <td><span class="status warning">{item['status']}</span></td>
            <td><button type="button" onclick="marcarAlertaLido('{item['tipo']}')">Marcar lido</button></td>
        </tr>
        """
        for item in ALERTAS
    )
    conteudo = f"""
    <section class="grid grid-3" aria-label="Resumo do familiar">
        <article class="card metric">
            <div>
                <strong>{len(ALERTAS)}</strong>
                <span>alertas para acompanhar</span>
            </div>
            <div class="icon">A</div>
        </article>
        <article class="card metric">
            <div>
                <strong>{len(MEDICAMENTOS)}</strong>
                <span>itens na rotina</span>
            </div>
            <div class="icon">R</div>
        </article>
        <article class="card metric">
            <div>
                <strong>Online</strong>
                <span>status do cuidado</span>
            </div>
            <div class="icon">O</div>
        </article>
    </section>
    <section class="grid grid-2">
        <article class="panel">
            <h1 class="section-title">Painel do familiar</h1>
            <p class="muted">Tela para acompanhar o paciente, receber alertas, falar com o profissional e autorizar atendimentos.</p>
            <div class="toolbar">
                <a href="/pacientes/rotina/medicamento"><button>Ver medicamentos</button></a>
                <button class="secondary" onclick="contatarProfissional()">Falar com profissional</button>
                <button onclick="autorizarAtendimento()">Autorizar atendimento</button>
            </div>
            <p id="mensagemFamiliar" class="message"></p>
        </article>
        <article class="panel">
            <h2 class="section-title">Dados do usuario</h2>
            <table>
                <tbody>
                    <tr><th>Nome</th><td id="dadosUsuarioNome">Responsavel familiar</td></tr>
                    <tr><th>Perfil</th><td id="dadosUsuarioPerfil">familiar</td></tr>
                    <tr><th>Email</th><td id="dadosUsuarioEmail">familiar@careonlive.com</td></tr>
                    <tr><th>Tela</th><td>Meu painel familiar</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h2 class="section-title">Dados do paciente</h2>
            <table>
                <tbody>
                    <tr><th>Paciente</th><td>Maria de Lourdes</td></tr>
                    <tr><th>Idade</th><td>75 anos</td></tr>
                    <tr><th>Cuidador</th><td>Cuidador demonstracao</td></tr>
                    <tr><th>Alertas</th><td>{len(ALERTAS)} registros</td></tr>
                    <tr><th>Ultima atualizacao</th><td>Rotina acompanhada hoje</td></tr>
                </tbody>
            </table>
        </article>
        <article class="panel">
            <h2 class="section-title">Familiares vinculados</h2>
            <table>
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Parentesco</th>
                        <th>Contato</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Responsavel familiar</td><td>Filho(a)</td><td>(61) 99999-0101</td><td><span class="status">Principal</span></td></tr>
                    <tr><td>Carlos Moura</td><td>Neto</td><td>(61) 99999-0202</td><td><span class="status">Autorizado</span></td></tr>
                    <tr><td>Ana Cristina</td><td>Irmã</td><td>(61) 99999-0303</td><td><span class="status">Autorizado</span></td></tr>
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
                    <th>Acao</th>
                </tr>
            </thead>
            <tbody>{linhas_alertas}</tbody>
        </table>
    </section>
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Medicamentos registrados do paciente</h2>
        <p class="muted">Acompanhamento da rotina de Maria de Lourdes com confirmacao de tomada e hora registrada.</p>
        {tabela_medicamentos_paciente("Maria de Lourdes")}
    </section>
    <section class="grid grid-2" style="margin-top:16px">
        <article class="panel">
            <h2 class="section-title">Mensagem para a equipe</h2>
            <form onsubmit="enviarMensagemFamiliar(); return false;">
                <label>Observacao da familia
                    <textarea id="mensagemEquipe" placeholder="Ex: gostaria de retorno sobre a pressao de hoje"></textarea>
                </label>
                <button type="button" onclick="enviarMensagemFamiliar()">Enviar para equipe</button>
            </form>
        </article>
    </section>
    <script>
        function contatarProfissional() {{
            const mensagem = document.getElementById('mensagemFamiliar');
            mensagem.className = 'message success';
            mensagem.innerText = 'Profissional notificado para retorno ao familiar.';
        }}
        function autorizarAtendimento() {{
            const mensagem = document.getElementById('mensagemFamiliar');
            mensagem.className = 'message success';
            mensagem.innerText = 'Atendimento autorizado pela familia.';
        }}
        function marcarAlertaLido(tipo) {{
            const mensagem = document.getElementById('mensagemFamiliar');
            mensagem.className = 'message success';
            mensagem.innerText = 'Alerta de ' + tipo + ' marcado como lido.';
        }}
        function enviarMensagemFamiliar() {{
            const texto = document.getElementById('mensagemEquipe').value;
            const mensagem = document.getElementById('mensagemFamiliar');
            if (!texto) {{
                mensagem.className = 'message error';
                mensagem.innerText = 'Escreva uma mensagem para a equipe.';
                return;
            }}
            mensagem.className = 'message success';
            mensagem.innerText = 'Mensagem enviada para a equipe de cuidado.';
            document.getElementById('mensagemEquipe').value = '';
        }}
        (function preencherDadosUsuario() {{
            try {{
                const usuario = JSON.parse(localStorage.getItem('careOnLiveUsuario'));
                if (!usuario) {{
                    return;
                }}
                document.getElementById('dadosUsuarioNome').innerText = usuario.nome || 'Responsavel familiar';
                document.getElementById('dadosUsuarioPerfil').innerText = usuario.perfil || 'familiar';
                document.getElementById('dadosUsuarioEmail').innerText = usuario.email || 'Email nao informado';
            }} catch (erro) {{}}
        }})();
    </script>
    """
    return pagina_base("Familiar", conteudo + modal_registrar_tomada() + script_exigir_perfil("familiar"))


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
                <a href="/cadastro"><button class="secondary">Criar cadastro</button></a>
                <a href="/pacientes/rotina/medicamento"><button class="secondary">Medicamentos</button></a>
            </div>
        </div>
        <article class="panel login-panel">
            <h1 class="section-title">Login Care on Live</h1>
            <form onsubmit="validarLogin(); return false;">
                <label>Email
                    <input type="text" id="email" autocomplete="username" />
                </label>
                <label>Senha
                    <input type="password" id="senha" autocomplete="current-password" />
                </label>
                <button id="btnEntrar" type="button" onclick="validarLogin()">Entrar</button>
                <div id="toast-mensagem" class="message" aria-live="polite"></div>
                <div id="atalho-dashboard" class="message"></div>
            </form>
            <section class="demo-access">
                <h2>Acessos de demonstracao</h2>
                <div class="demo-access-list">
                    <div class="demo-access-item">
                        <div>
                            <strong>Admin</strong>
                            <span>admin@careonlive.com</span>
                            <span>Senha: admin123</span>
                        </div>
                        <button type="button" onclick="preencherLogin('admin@careonlive.com', 'admin123')">Usar</button>
                    </div>
                    <div class="demo-access-item">
                        <div>
                            <strong>Profissional/cuidador</strong>
                            <span>cuidador@careonlive.com</span>
                            <span>Senha: senhaSegura123</span>
                        </div>
                        <button type="button" onclick="preencherLogin('cuidador@careonlive.com', 'senhaSegura123')">Usar</button>
                    </div>
                    <div class="demo-access-item">
                        <div>
                            <strong>Paciente</strong>
                            <span>paciente@careonlive.com</span>
                            <span>Senha: paciente123</span>
                        </div>
                        <button type="button" onclick="preencherLogin('paciente@careonlive.com', 'paciente123')">Usar</button>
                    </div>
                    <div class="demo-access-item">
                        <div>
                            <strong>Familiar/responsavel</strong>
                            <span>familiar@careonlive.com</span>
                            <span>Senha: familiar123</span>
                        </div>
                        <button type="button" onclick="preencherLogin('familiar@careonlive.com', 'familiar123')">Usar</button>
                    </div>
                </div>
            </section>
            <p class="muted" style="margin-top:16px">Ainda nao tem conta? <a href="/cadastro">Criar cadastro</a></p>
            <p class="muted">Quer contratar alguem? <a href="/profissionais">Ver profissionais disponiveis</a></p>
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
                localStorage.setItem('careOnLiveUsuario', JSON.stringify(dados.usuario));
                window.location.href = dados.usuario.dashboard;
                return;
            }}

            msg.className = 'message error';
            msg.innerText = dados.mensagem;
        }}
        function preencherLogin(email, senha) {{
            document.getElementById('email').value = email;
            document.getElementById('senha').value = senha;
            document.getElementById('toast-mensagem').className = 'message';
            document.getElementById('toast-mensagem').innerText = 'Acesso preenchido. Clique em Entrar.';
        }}
    </script>
    {script_redirecionar_usuario_logado()}
    """
    return pagina_base("Login", conteudo)


@app.get("/", response_class=HTMLResponse)
def tela_home():
    conteudo = """
    <section class="grid grid-2">
        <article class="panel">
            <h1 class="section-title">Care on Live</h1>
            <p class="muted">Plataforma para conectar pacientes, familiares e profissionais em uma rotina de cuidado domiciliar.</p>
            <div class="toolbar">
                <a href="/login"><button>Entrar</button></a>
                <a href="/cadastro"><button class="secondary">Criar cadastro</button></a>
                <a href="/profissionais"><button class="secondary">Ver profissionais</button></a>
            </div>
        </article>
        <article class="panel">
            <h2 class="section-title">Como funciona</h2>
            <table>
                <tbody>
                    <tr><th>Paciente</th><td>Acompanha remedios, rotina e pedidos de ajuda.</td></tr>
                    <tr><th>Familiar</th><td>Recebe alertas, acompanha cuidado e fala com a equipe.</td></tr>
                    <tr><th>Profissional</th><td>Gerencia pacientes, mensagens, prescricoes e solicitacoes.</td></tr>
                </tbody>
            </table>
        </article>
    </section>
    <section class="grid grid-3" style="margin-top:16px">
        <article class="card metric">
            <div>
                <strong>24h</strong>
                <span>apoio ao cuidado</span>
            </div>
            <div class="icon">C</div>
        </article>
        <article class="card metric">
            <div>
                <strong>3</strong>
                <span>perfis de usuario</span>
            </div>
            <div class="icon">U</div>
        </article>
        <article class="card metric">
            <div>
                <strong>SOS</strong>
                <span>acionamento rapido</span>
            </div>
            <div class="icon">S</div>
        </article>
    </section>
    """
    return pagina_base("Home", conteudo)


@app.get("/cadastro", response_class=HTMLResponse)
def tela_cadastro():
    conteudo = """
    <section class="login-layout">
        <div class="login-intro">
            <div class="logo-large">CL+</div>
            <div>
                <h1>Criar cadastro</h1>
                <p class="muted">Cadastre um acesso para acompanhar cuidados, rotina, pacientes e profissionais.</p>
            </div>
            <div class="toolbar">
                <a href="/login"><button>Ja tenho login</button></a>
                <a href="/profissionais"><button class="secondary">Ver profissionais</button></a>
            </div>
        </div>
        <article class="panel login-panel">
            <h1 class="section-title">Cadastro Care on Live</h1>
            <form onsubmit="validarCadastro(); return false;">
                <label>Nome
                    <input type="text" id="nomeCadastro" autocomplete="name" />
                </label>
                <label>Email
                    <input type="text" id="emailCadastro" autocomplete="email" />
                </label>
                <label>Senha
                    <input type="password" id="senhaCadastro" autocomplete="new-password" />
                </label>
                <label>Tipo de usuario
                    <select id="perfilCadastro">
                        <option value="">Selecione o tipo de usuario</option>
                        <option value="paciente">Paciente</option>
                        <option value="familiar">Familiar</option>
                        <option value="profissional">Profissional</option>
                    </select>
                </label>
                <button id="btnCadastrar" type="button" onclick="validarCadastro()">Cadastrar</button>
                <div id="mensagemCadastro" class="message" aria-live="polite"></div>
                <div id="atalhoCadastro" class="message"></div>
            </form>
        </article>
    </section>
    <script>
        async function validarCadastro() {
            var nome = document.getElementById('nomeCadastro').value;
            var email = document.getElementById('emailCadastro').value;
            var senha = document.getElementById('senhaCadastro').value;
            var perfil = document.getElementById('perfilCadastro').value;
            var msg = document.getElementById('mensagemCadastro');
            var atalho = document.getElementById('atalhoCadastro');
            msg.className = 'message';
            atalho.innerHTML = '';

            if (!nome) {
                msg.className = 'message error';
                msg.innerText = 'Nome obrigat\u00f3rio';
                return;
            }
            if (!email) {
                msg.className = 'message error';
                msg.innerText = 'Email obrigat\u00f3rio';
                return;
            }
            if (!senha) {
                msg.className = 'message error';
                msg.innerText = 'Senha obrigat\u00f3ria';
                return;
            }
            if (senha.length < 6) {
                msg.className = 'message error';
                msg.innerText = 'Senha deve ter pelo menos 6 caracteres';
                return;
            }
            if (!perfil) {
                msg.className = 'message error';
                msg.innerText = 'Selecione o tipo de usuario';
                return;
            }

            const resposta = await fetch('/api/cadastro', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome: nome, email: email, senha: senha, perfil: perfil })
            });
            const dados = await resposta.json();

            if (resposta.ok) {
                msg.className = 'message success';
                msg.innerText = dados.mensagem;
                localStorage.setItem('careOnLiveUsuario', JSON.stringify(dados.usuario));
                window.location.href = dados.usuario.dashboard;
                return;
            }

            msg.className = 'message error';
            msg.innerText = dados.mensagem;
        }
    </script>
    """ + script_redirecionar_usuario_logado() + """
    """
    return pagina_base("Cadastro", conteudo)


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
    <section class="panel" style="margin-top:16px">
        <h2 class="section-title">Medicamentos registrados do paciente</h2>
        <p class="muted">Lista completa da rotina de Maria de Lourdes, com confirmacao se tomou e hora registrada.</p>
        <p id="mensagemMedicamentos" class="message"></p>
        """ + tabela_medicamentos_paciente("Maria de Lourdes") + """
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
            var corpoTabela = document.querySelector('section.panel tbody');
            if (corpoTabela) {
                corpoTabela.innerHTML += '<tr><td>Maria de Lourdes</td><td>' + nome + '</td><td>' + horario + '</td><td>' + Number(qtd) + '</td><td><span class="status warning">Nao</span></td><td>Aguardando</td><td>Agendado</td><td><button type="button" onclick="abrirModalTomada(\\'novo\\', \\''
                    + nome.replace(/'/g, '') + '\\')">Registrar tomada</button></td></tr>';
            }
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
    return pagina_base("Medicamentos", conteudo + modal_registrar_tomada())
