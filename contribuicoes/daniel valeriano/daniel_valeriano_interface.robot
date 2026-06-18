*** Settings ***
Library          SeleniumLibrary
Test Teardown    Close Browser

*** Variables ***
${BROWSER}              chrome
${URL_CADASTRO}         http://localhost:3000/cadastro
${URL_LOGIN}            http://localhost:3000/login
${INPUT_NOME}           id=nomeCadastro
${INPUT_EMAIL_CAD}      id=emailCadastro
${INPUT_SENHA_CAD}      id=senhaCadastro
${SELECT_PERFIL}        id=perfilCadastro
${BOTAO_CADASTRAR}      id=btnCadastrar
${MENSAGEM_CADASTRO}    id=mensagemCadastro
${INPUT_EMAIL}          id=email
${INPUT_SENHA}          id=senha
${BOTAO_ENTRAR}         id=btnEntrar

*** Test Cases ***
CT01 - Deve exibir opcoes de tipo de usuario no cadastro
    Dado que o usuario acessa a tela de cadastro
    Entao a pagina deve conter o texto    Cadastro Care on Live
    E a pagina deve conter o texto    Selecione o tipo de usuario
    E a pagina deve conter o texto    Paciente
    E a pagina deve conter o texto    Familiar
    E a pagina deve conter o texto    Profissional

CT02 - Deve bloquear cadastro com senha curta
    Dado que o usuario acessa a tela de cadastro
    Input Text    ${INPUT_NOME}    Usuario Teste
    Input Text    ${INPUT_EMAIL_CAD}    usuario.teste@careonlive.com
    Input Password    ${INPUT_SENHA_CAD}    123
    Select From List By Value    ${SELECT_PERFIL}    familiar
    Click Button    ${BOTAO_CADASTRAR}
    Wait Until Element Contains    ${MENSAGEM_CADASTRO}    Senha deve ter pelo menos 6 caracteres    timeout=5s

CT03 - Deve abrir painel do paciente apos login
    Dado que o usuario faz login como paciente
    Entao a pagina deve conter o texto    Painel do paciente
    E a pagina deve conter o texto    Meus medicamentos
    E a pagina deve conter o texto    Contatos de apoio

CT04 - Deve abrir modal de tomada no painel do paciente
    Dado que o usuario faz login como paciente
    Click Button    Registrar tomada
    Entao a pagina deve conter o texto    Hora da tomada

*** Keywords ***
Dado que o usuario acessa a tela de cadastro
    Open Browser    ${URL_CADASTRO}    ${BROWSER}
    Maximize Browser Window

Dado que o usuario faz login como paciente
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    Maximize Browser Window
    Input Text    ${INPUT_EMAIL}    paciente@careonlive.com
    Input Password    ${INPUT_SENHA}    paciente123
    Click Button    ${BOTAO_ENTRAR}
    Wait Until Location Contains    /paciente    timeout=5s

Entao a pagina deve conter o texto
    [Arguments]    ${texto}
    Page Should Contain    ${texto}

E a pagina deve conter o texto
    [Arguments]    ${texto}
    Page Should Contain    ${texto}

