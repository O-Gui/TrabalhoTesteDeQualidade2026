*** Settings ***
Library          SeleniumLibrary
Test Teardown    Close Browser

*** Variables ***
# Configurações Gerais
${BROWSER}                 chrome

# Variáveis - Tela de Login
${URL_LOGIN}               http://localhost:3000/login
${INPUT_EMAIL}             id=email
${INPUT_SENHA}             id=senha
${BOTAO_ENTRAR}            id=btnEntrar
${MENSAGEM_LOGIN}          id=toast-mensagem

# Variáveis - Tela de Cadastro de Medicamento
${URL_MEDICAMENTO}         http://localhost:3000/pacientes/rotina/medicamento
${INPUT_NOME_REM}          id=nomeRemedio
${INPUT_HORARIO}           id=horarioRemedio
${INPUT_QTD}               id=quantidadeRemedio
${BOTAO_SALVAR}            id=btnSalvarMedicamento
${MENSAGEM_MEDICAMENTO}    id=alertaFormulario

*** Test Cases ***
# ==========================================
# SUÍTE 01: LOGIN NA PLATAFORMA
# ==========================================
CT01 - Deve realizar login com credenciais válidas
    Dado que o usuário acessa a tela de login
    E informa o email    cuidador@careonlive.com
    E informa a senha    senhaSegura123
    Quando solicitar o login
    Então o sistema deve apresentar a mensagem de login    Login realizado com sucesso

CT02 - Deve validar email obrigatório
    Dado que o usuário acessa a tela de login
    E informa o email    ${EMPTY}
    E informa a senha    senhaSegura123
    Quando solicitar o login
    Então o sistema deve apresentar a mensagem de login    Email obrigatório

CT03 - Deve validar senha obrigatória
    Dado que o usuário acessa a tela de login
    E informa o email    cuidador@careonlive.com
    E informa a senha    ${EMPTY}
    Quando solicitar o login
    Então o sistema deve apresentar a mensagem de login    Senha obrigatória

CT04 - Deve bloquear login com credenciais inexistentes
    Dado que o usuário acessa a tela de login
    E informa o email    erro@careonlive.com
    E informa a senha    senhaErrada
    Quando solicitar o login
    Então o sistema deve apresentar a mensagem de login    Credenciais inválidas

# ==========================================
# SUÍTE 02: CADASTRO DE MEDICAMENTO
# ==========================================
CT05 - Deve salvar rotina de medicamento com dados válidos
    Dado que o usuário acessa a tela de cadastro de medicamento
    E informa o nome do remédio    Losartana 50mg
    E informa o horário    08:00
    E informa a quantidade    1
    Quando solicitar o salvamento
    Então o sistema deve apresentar a mensagem no formulário    Medicação salva na rotina

CT06 - Deve validar obrigatoriedade do nome do remédio
    Dado que o usuário acessa a tela de cadastro de medicamento
    E informa o nome do remédio    ${EMPTY}
    E informa o horário    08:00
    E informa a quantidade    1
    Quando solicitar o salvamento
    Então o sistema deve apresentar a mensagem no formulário    Nome do medicamento obrigatório

CT07 - Deve validar obrigatoriedade do horário
    Dado que o usuário acessa a tela de cadastro de medicamento
    E informa o nome do remédio    Losartana 50mg
    E informa o horário    ${EMPTY}
    E informa a quantidade    1
    Quando solicitar o salvamento
    Então o sistema deve apresentar a mensagem no formulário    Horário obrigatório

CT08 - Deve bloquear quantidade zerada
    Dado que o usuário acessa a tela de cadastro de medicamento
    E informa o nome do remédio    Losartana 50mg
    E informa o horário    08:00
    E informa a quantidade    0
    Quando solicitar o salvamento
    Então o sistema deve apresentar a mensagem no formulário    A quantidade deve ser maior que zero

*** Keywords ***
# ------------------------------------------
# Keywords - Login
# ------------------------------------------
Dado que o usuário acessa a tela de login
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    Maximize Browser Window

E informa o email
    [Arguments]    ${email}
    Input Text    ${INPUT_EMAIL}    ${email}

E informa a senha
    [Arguments]    ${senha}
    Input Password    ${INPUT_SENHA}    ${senha}

Quando solicitar o login
    Click Button    ${BOTAO_ENTRAR}

Então o sistema deve apresentar a mensagem de login
    [Arguments]    ${mensagem_esperada}
    Element Text Should Be    ${MENSAGEM_LOGIN}    ${mensagem_esperada}

# ------------------------------------------
# Keywords - Cadastro de Medicamento
# ------------------------------------------
Dado que o usuário acessa a tela de cadastro de medicamento
    Open Browser    ${URL_MEDICAMENTO}    ${BROWSER}
    Maximize Browser Window

E informa o nome do remédio
    [Arguments]    ${nome}
    Input Text    ${INPUT_NOME_REM}    ${nome}

E informa o horário
    [Arguments]    ${horario}
    Input Text    ${INPUT_HORARIO}    ${horario}

E informa a quantidade
    [Arguments]    ${qtd}
    Input Text    ${INPUT_QTD}    ${qtd}

Quando solicitar o salvamento
    Click Button    ${BOTAO_SALVAR}

Então o sistema deve apresentar a mensagem no formulário
    [Arguments]    ${mensagem_esperada}
    Element Text Should Be    ${MENSAGEM_MEDICAMENTO}    ${mensagem_esperada}
