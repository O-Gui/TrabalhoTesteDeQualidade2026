*** Settings ***
Library          SeleniumLibrary
Test Teardown    Close Browser

*** Variables ***
${BROWSER}                 chrome
${URL_MEDICAMENTO}         http://localhost:3000/pacientes/rotina/medicamento
${URL_LOGIN}               http://localhost:3000/login
${URL_FAMILIAR}            http://localhost:3000/familiar
${INPUT_EMAIL}             id=email
${INPUT_SENHA}             id=senha
${BOTAO_ENTRAR}            id=btnEntrar
${INPUT_NOME_REM}          id=nomeRemedio
${INPUT_HORARIO}           id=horarioRemedio
${INPUT_QTD}               id=quantidadeRemedio
${BOTAO_SALVAR}            id=btnSalvarMedicamento
${MENSAGEM_MEDICAMENTO}    id=alertaFormulario

*** Test Cases ***
CT01 - Deve salvar medicamento com dados validos
    Dado que o usuario acessa a tela de medicamento
    E informa o nome do remedio    Losartana 50mg
    E informa o horario    08:00
    E informa a quantidade    1
    Quando solicitar o salvamento
    Entao o sistema deve apresentar a mensagem no formulario    Medicação salva na rotina

CT02 - Deve bloquear medicamento com quantidade zerada
    Dado que o usuario acessa a tela de medicamento
    E informa o nome do remedio    Losartana 50mg
    E informa o horario    08:00
    E informa a quantidade    0
    Quando solicitar o salvamento
    Entao o sistema deve apresentar a mensagem no formulario    A quantidade deve ser maior que zero

CT03 - Deve exibir medicamentos no painel familiar
    Dado que o usuario acessa o painel familiar
    Entao a pagina deve conter o texto    Medicamentos registrados do paciente
    E a pagina deve conter o texto    Tomou?
    E a pagina deve conter o texto    Hora registrada

CT04 - Deve abrir modal para registrar tomada
    Dado que o usuario acessa o painel familiar
    Quando clicar em registrar tomada
    Entao a pagina deve conter o texto    Hora da tomada

*** Keywords ***
Dado que o usuario acessa a tela de medicamento
    Open Browser    ${URL_MEDICAMENTO}    ${BROWSER}
    Maximize Browser Window
    Page Should Contain    Cadastro de Medicamento

Dado que o usuario acessa o painel familiar
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    Maximize Browser Window
    Input Text    ${INPUT_EMAIL}    familiar@careonlive.com
    Input Password    ${INPUT_SENHA}    familiar123
    Click Button    ${BOTAO_ENTRAR}
    Wait Until Location Contains    /familiar    timeout=5s
    Page Should Contain    Painel do familiar

E informa o nome do remedio
    [Arguments]    ${nome}
    Input Text    ${INPUT_NOME_REM}    ${nome}

E informa o horario
    [Arguments]    ${horario}
    Input Text    ${INPUT_HORARIO}    ${horario}

E informa a quantidade
    [Arguments]    ${qtd}
    Input Text    ${INPUT_QTD}    ${qtd}

Quando solicitar o salvamento
    Click Button    ${BOTAO_SALVAR}

Quando clicar em registrar tomada
    Click Button    Registrar tomada

Entao o sistema deve apresentar a mensagem no formulario
    [Arguments]    ${mensagem_esperada}
    Wait Until Element Contains    ${MENSAGEM_MEDICAMENTO}    ${mensagem_esperada}    timeout=5s

Entao a pagina deve conter o texto
    [Arguments]    ${texto}
    Page Should Contain    ${texto}

E a pagina deve conter o texto
    [Arguments]    ${texto}
    Page Should Contain    ${texto}
