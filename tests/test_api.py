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


def test_login_mostra_acessos_de_demonstracao():
    resposta = client.get("/login")

    assert resposta.status_code == 200
    assert "Acessos de demonstracao" in resposta.text
    assert "admin@careonlive.com" in resposta.text
    assert "admin123" in resposta.text
    assert "cuidador@careonlive.com" in resposta.text
    assert "senhaSegura123" in resposta.text
    assert "paciente@careonlive.com" in resposta.text
    assert "paciente123" in resposta.text
    assert "familiar@careonlive.com" in resposta.text
    assert "familiar123" in resposta.text
    assert "Criar cadastro" in resposta.text


def test_home_abre_tela_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert "Plataforma para conectar pacientes" in resposta.text
    assert "Como funciona" in resposta.text
    assert "Login Care on Live" not in resposta.text


def test_login_abre_tela_de_login():
    resposta = client.get("/login")

    assert resposta.status_code == 200
    assert "Login Care on Live" in resposta.text
    assert "CL+" in resposta.text


def test_pagina_cadastro_disponivel():
    resposta = client.get("/cadastro")

    assert resposta.status_code == 200
    assert "Cadastro Care on Live" in resposta.text
    assert 'id="nomeCadastro"' in resposta.text
    assert 'id="emailCadastro"' in resposta.text
    assert 'id="senhaCadastro"' in resposta.text
    assert "Selecione o tipo de usuario" in resposta.text
    assert '<option value="paciente">Paciente</option>' in resposta.text
    assert '<option value="familiar">Familiar</option>' in resposta.text
    assert '<option value="profissional">Profissional</option>' in resposta.text


def test_cadastro_usuario_sucesso_e_login():
    email = "novo.familiar@careonlive.com"
    USUARIOS.pop(email, None)

    resposta = client.post(
        "/api/cadastro",
        json={
            "nome": "Novo Familiar",
            "email": email,
            "senha": "senha123",
            "perfil": "familiar",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["mensagem"] == "Cadastro realizado com sucesso"
    assert resposta.json()["usuario"]["dashboard"] == "/familiar"

    login = client.post("/api/login", json={"email": email, "senha": "senha123"})

    assert login.status_code == 200
    assert login.json()["usuario"]["perfil"] == "familiar"


def test_cadastro_usuario_email_repetido():
    resposta = client.post(
        "/api/cadastro",
        json={
            "nome": "Administrador Duplicado",
            "email": "admin@careonlive.com",
            "senha": "senha123",
            "perfil": "administrador",
        },
    )

    assert resposta.status_code == 409
    assert resposta.json()["mensagem"] == "Email j\u00e1 cadastrado"


def test_cadastro_publico_nao_permite_administrador():
    resposta = client.post(
        "/api/cadastro",
        json={
            "nome": "Admin Publico",
            "email": "admin.publico@careonlive.com",
            "senha": "senha123",
            "perfil": "administrador",
        },
    )

    assert resposta.status_code == 400
    assert resposta.json()["mensagem"] == "Perfil inv\u00e1lido"


def test_menu_publico_nao_expoe_paineis_de_perfil():
    resposta = client.get("/login")

    assert resposta.status_code == 200
    assert 'href="/admin"' not in resposta.text
    assert 'href="/paciente"' not in resposta.text
    assert 'href="/familiar"' not in resposta.text
    assert 'href="/profissional"' not in resposta.text
    assert 'href="/profissionais"' in resposta.text
    assert 'href="/docs"' not in resposta.text
    assert ">API<" not in resposta.text


def test_api_profissionais_populada():
    resposta = client.get("/api/profissionais")

    assert resposta.status_code == 200
    assert resposta.json()["total"] == len(PROFISSIONAIS)
    assert resposta.json()["total"] >= 4


def test_marketplace_profissionais():
    resposta = client.get("/profissionais")

    assert resposta.status_code == 200
    assert "Profissionais disponiveis" in resposta.text
    assert "Marketplace" not in resposta.text
    assert "Selecionar profissional" in resposta.text
    assert "mailto:" in resposta.text


def test_pdf_acessos_sem_404():
    resposta = client.get("/acessos-care-on-live.pdf")

    assert resposta.status_code == 200
    assert resposta.headers["content-type"] == "application/pdf"


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


def test_painel_profissional_tem_funcionalidades_proprias():
    resposta = client.get("/profissional")

    assert resposta.status_code == 200
    assert "Registrar sinais vitais" in resposta.text
    assert "Registro de evolucao" in resposta.text
    assert "Solicitacoes de servico" in resposta.text
    assert "Aceitar" in resposta.text
    assert "Recusar" in resposta.text
    assert "Meus pacientes" in resposta.text
    assert "Passar remedio para paciente" in resposta.text
    assert "Conversa com paciente" in resposta.text
    assert "Mensagem para familia" in resposta.text


def test_painel_admin_tem_visao_completa_do_sistema():
    resposta = client.get("/admin")

    assert resposta.status_code == 200
    assert "Visualizacao completa do sistema" in resposta.text
    assert "Usuarios cadastrados" in resposta.text
    assert "Profissionais cadastrados" in resposta.text
    assert "Pacientes demonstrativos" in resposta.text
    assert "Servicos publicados" in resposta.text
    assert "Medicamentos registrados" in resposta.text
    assert "Alertas e ocorrencias" in resposta.text
    assert "Gerar relatorio" in resposta.text


def test_painel_paciente_tem_funcionalidades_proprias():
    resposta = client.get("/paciente")

    assert resposta.status_code == 200
    assert "Pedir ajuda" in resposta.text
    assert "Estou bem" in resposta.text
    assert "Chamar cuidador" in resposta.text
    assert "Dados do usuario" in resposta.text
    assert "Dados de cuidado" in resposta.text
    assert "Contatos de apoio" in resposta.text
    assert "Meus medicamentos" in resposta.text
    assert "Tomou?" in resposta.text
    assert "Hora da tomada" in resposta.text
    assert "Mensagem para o cuidador" in resposta.text
    assert "Mensagem para familia" in resposta.text
    assert "Historico rapido" in resposta.text


def test_painel_familiar_tem_funcionalidades_proprias():
    resposta = client.get("/familiar")

    assert resposta.status_code == 200
    assert "Falar com profissional" in resposta.text
    assert "Autorizar atendimento" in resposta.text
    assert "Mensagem para a equipe" in resposta.text
    assert "Dados do usuario" in resposta.text
    assert "Familiares vinculados" in resposta.text
    assert "Medicamentos registrados do paciente" in resposta.text
    assert "Tomou?" in resposta.text
    assert "Hora registrada" in resposta.text
    assert "Registrar tomada" in resposta.text
    assert "Hora da tomada" in resposta.text


def test_pagina_medicamentos_mostra_registro_de_tomada():
    resposta = client.get("/pacientes/rotina/medicamento")

    assert resposta.status_code == 200
    assert "Medicamentos registrados do paciente" in resposta.text
    assert "Tomou?" in resposta.text
    assert "Hora registrada" in resposta.text
    assert "Registrar tomada" in resposta.text
    assert "Hora da tomada" in resposta.text
