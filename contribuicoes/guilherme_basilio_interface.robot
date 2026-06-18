*** Settings ***
Library          SeleniumLibrary
Test Teardown    Close Browser

*** Variables ***
${BROWSER}          chrome
${URL_LOGIN}        http://localhost:3000/login
${INPUT_EMAIL}      id=email
${INPUT_SENHA}      id=senha
${BOTAO_ENTRAR}     id=btnEntrar

*** Test Cases ***
CT01 - Deve exibir solicitacoes no painel profissional
    Dado que o usuario faz login como profissional
    Entao a pagina deve conter o texto    Painel do profissional
    E a pagina deve conter o texto    Solicitacoes de servico
    E a pagina deve conter o texto    Aceitar
    E a pagina deve conter o texto    Recusar
    E a pagina deve conter o texto    Meus pacientes

CT02 - Deve aceitar uma solicitacao de servico
    Dado que o usuario faz login como profissional
    Click Button    Aceitar
    Entao a pagina deve conter o texto    Aceita

CT03 - Deve exibir visao completa no painel admin
    Dado que o usuario faz login como admin
    Entao a pagina deve conter o texto    Painel do administrador
    E a pagina deve conter o texto    Usuarios cadastrados
    E a pagina deve conter o texto    Servicos publicados
    E a pagina deve conter o texto    Medicamentos registrados
    E a pagina deve conter o texto    Alertas e ocorrencias

CT04 - Deve gerar relatorio administrativo
    Dado que o usuario faz login como admin
    Click Button    Gerar relatorio
    Entao a pagina deve conter o texto    Relatorio administrativo gerado para conferencia

*** Keywords ***
Dado que o usuario faz login como profissional
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    Maximize Browser Window
    Input Text    ${INPUT_EMAIL}    cuidador@careonlive.com
    Input Password    ${INPUT_SENHA}    senhaSegura123
    Click Button    ${BOTAO_ENTRAR}
    Wait Until Location Contains    /profissional    timeout=5s

Dado que o usuario faz login como admin
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    Maximize Browser Window
    Input Text    ${INPUT_EMAIL}    admin@careonlive.com
    Input Password    ${INPUT_SENHA}    admin123
    Click Button    ${BOTAO_ENTRAR}
    Wait Until Location Contains    /admin    timeout=5s

Entao a pagina deve conter o texto
    [Arguments]    ${texto}
    Page Should Contain    ${texto}

E a pagina deve conter o texto
    [Arguments]    ${texto}
    Page Should Contain    ${texto}

