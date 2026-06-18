*** Settings ***
Library          SeleniumLibrary
Test Teardown    Close Browser

*** Variables ***
${BROWSER}                 chrome
${URL_LOGIN}               http://localhost:3000/login
${URL_PROFISSIONAIS}       http://localhost:3000/profissionais
${INPUT_EMAIL}             id=email
${INPUT_SENHA}             id=senha
${BOTAO_ENTRAR}            id=btnEntrar
${MENSAGEM_LOGIN}          id=toast-mensagem

*** Test Cases ***
CT01 - Deve realizar login de profissional com credenciais validas
    Dado que o usuario acessa a tela de login
    E informa o email    cuidador@careonlive.com
    E informa a senha    senhaSegura123
    Quando solicitar o login
    Entao o sistema deve abrir o painel do profissional

CT02 - Deve bloquear login com credenciais invalidas
    Dado que o usuario acessa a tela de login
    E informa o email    erro@careonlive.com
    E informa a senha    senhaErrada
    Quando solicitar o login
    Entao o sistema deve apresentar a mensagem de login    Credenciais inválidas

CT03 - Deve exibir a tela de profissionais disponiveis
    Dado que o usuario acessa a tela de profissionais
    Entao a pagina deve conter o texto    Profissionais disponiveis
    E a pagina deve conter o texto    Selecionar profissional

CT04 - Deve exibir contato por email na tela de profissionais
    Dado que o usuario acessa a tela de profissionais
    Entao a pagina deve conter link de contato por email

*** Keywords ***
Dado que o usuario acessa a tela de login
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    Maximize Browser Window
    Page Should Contain    Login Care on Live

Dado que o usuario acessa a tela de profissionais
    Open Browser    ${URL_PROFISSIONAIS}    ${BROWSER}
    Maximize Browser Window

E informa o email
    [Arguments]    ${email}
    Input Text    ${INPUT_EMAIL}    ${email}

E informa a senha
    [Arguments]    ${senha}
    Input Password    ${INPUT_SENHA}    ${senha}

Quando solicitar o login
    Click Button    ${BOTAO_ENTRAR}

Entao o sistema deve apresentar a mensagem de login
    [Arguments]    ${mensagem_esperada}
    Wait Until Element Contains    ${MENSAGEM_LOGIN}    ${mensagem_esperada}    timeout=5s

Entao o sistema deve abrir o painel do profissional
    Wait Until Location Contains    /profissional    timeout=5s
    Page Should Contain    Painel do profissional

Entao a pagina deve conter o texto
    [Arguments]    ${texto}
    Page Should Contain    ${texto}

E a pagina deve conter o texto
    [Arguments]    ${texto}
    Page Should Contain    ${texto}

Entao a pagina deve conter link de contato por email
    Page Should Contain Element    xpath=//a[contains(@href, 'mailto:')]
