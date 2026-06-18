from fastapi.testclient import TestClient

from care_on_live_app import PROFISSIONAIS, USUARIOS, app


client = TestClient(app)


def test_health_online():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "online"


def test_login_valido():
    resposta = client.post(
        "/api/login",
        json={"email": "cuidador@careonlive.com", "senha": "senhaSegura123"},
    )

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Login realizado com sucesso"
    assert resposta.json()["usuario"]["perfil"] == "profissional"


def test_login_por_perfil():
    credenciais = [
        ("admin@careonlive.com", "admin123", "administrador", "/admin"),
        ("cuidador@careonlive.com", "senhaSegura123", "profissional", "/profissional"),
        ("paciente@careonlive.com", "paciente123", "paciente", "/paciente"),
        ("familiar@careonlive.com", "familiar123", "familiar", "/familiar"),
    ]

    for email, senha, perfil, dashboard in credenciais:
        resposta = client.post("/api/login", json={"email": email, "senha": senha})

        assert resposta.status_code == 200
        assert resposta.json()["usuario"]["perfil"] == perfil
        assert resposta.json()["usuario"]["dashboard"] == dashboard


def test_login_nao_expoe_credenciais_na_tela():
    resposta = client.get("/login")

    assert resposta.status_code == 200
    for email, usuario in USUARIOS.items():
        assert email not in resposta.text
        assert usuario["senha"] not in resposta.text


def test_api_profissionais_populada():
    resposta = client.get("/api/profissionais")

    assert resposta.status_code == 200
    assert resposta.json()["total"] == len(PROFISSIONAIS)
    assert resposta.json()["total"] >= 4


def test_cadastro_paciente_idade_invalida():
    resposta = client.post(
        "/pacientes",
        json={
            "nome": "Joao Batista",
            "idade": -5,
            "necessidadePrincipal": "Acompanhamento de medicacao",
        },
    )

    assert resposta.status_code == 400
    assert resposta.json()["codigoErro"] == "IDADE_INVALIDA"


def test_cadastro_paciente_sucesso():
    resposta = client.post(
        "/pacientes",
        json={
            "nome": "Maria de Lourdes",
            "idade": 75,
            "necessidadePrincipal": "Monitoramento continuo SOS",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["mensagem"] == "Registrado com sucesso"


def test_publicar_servico_com_preco_fora_do_limite():
    resposta = client.post(
        "/servicos",
        json={
            "idProfissional": "COREN-DF-12345",
            "titulo": "Cuidador noturno",
            "precoTurno": 49.99,
        },
    )

    assert resposta.status_code == 400
    assert resposta.json()["codigoErro"] == "PRECO_FORA_DO_LIMITE"


def test_salvar_medicamento():
    resposta = client.post(
        "/medicamentos",
        json={
            "paciente": "Maria de Lourdes",
            "nomeRemedio": "Losartana 50mg",
            "horarioRemedio": "08:00",
            "quantidadeRemedio": 1,
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["mensagem"] == "Medicação salva na rotina"


def test_acionar_sos():
    resposta = client.post(
        "/sos",
        json={"paciente": "Maria de Lourdes", "localizacao": "Residencia"},
    )

    assert resposta.status_code == 201
    assert resposta.json()["dados"]["tipo"] == "SOS"


def test_paginas_por_perfil():
    paginas = {
        "/admin": "Painel do administrador",
        "/profissional": "Painel do profissional",
        "/paciente": "Painel do paciente",
        "/familiar": "Painel do familiar",
    }

    for url, texto in paginas.items():
        resposta = client.get(url)

        assert resposta.status_code == 200
        assert texto in resposta.text
