# Care on Live

Sistema academico para gestao e monitoramento inteligente de cuidados com idosos.

## O que esta pronto

- Site web com painel operacional.
- Tela de login validavel por teste automatizado.
- Tela de cadastro de medicamento.
- API REST com rotas de pacientes, servicos, medicamentos, alertas e SOS.
- Documentacao interativa da API pelo Swagger.
- Testes automatizados de API com pytest.
- Colecao Postman e suite Robot Framework mantidas no repositorio.
- Versao estatica pronta para GitHub Pages na pasta `docs/`.
- PDF separado com os acessos de demonstracao.

## Como rodar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_all.py
```

## URLs principais

- Site: http://127.0.0.1:3000
- Login: http://127.0.0.1:3000/login
- Painel administrador: http://127.0.0.1:3000/admin
- Painel profissional/cuidador: http://127.0.0.1:3000/profissional
- Painel paciente: http://127.0.0.1:3000/paciente
- Painel familiar: http://127.0.0.1:3000/familiar
- Cadastro de medicamento: http://127.0.0.1:3000/pacientes/rotina/medicamento
- API: http://127.0.0.1:8080
- Swagger/API Docs: http://127.0.0.1:8080/docs

## GitHub Pages

A pasta `docs/` contem a versao estatica para publicar no GitHub Pages.

URL esperada depois de ativar o Pages:

https://o-gui.github.io/TrabalhoTesteDeQualidade2026/

Links separados:

- Inicio: https://o-gui.github.io/TrabalhoTesteDeQualidade2026/
- Admin: https://o-gui.github.io/TrabalhoTesteDeQualidade2026/admin.html
- Profissionais: https://o-gui.github.io/TrabalhoTesteDeQualidade2026/profissionais.html
- Pacientes: https://o-gui.github.io/TrabalhoTesteDeQualidade2026/pacientes.html
- Familiar: https://o-gui.github.io/TrabalhoTesteDeQualidade2026/familiar.html
- Medicamentos: https://o-gui.github.io/TrabalhoTesteDeQualidade2026/medicamentos.html
- PDF de acessos: https://o-gui.github.io/TrabalhoTesteDeQualidade2026/acessos-care-on-live.pdf

## Credenciais de demonstracao

As credenciais nao ficam expostas nas telas. Elas foram separadas no PDF:

`docs/acessos-care-on-live.pdf`

## Testes

```powershell
pytest
```

Para a suite web em Robot Framework, deixe o site rodando na porta `3000` e execute:

```powershell
robot teste.robot
```

## Wiki

Toda a documentacao de analise e controle de risco esta organizada na Wiki:

https://github.com/O-Gui/TrabalhoTesteDeQualidade2026/wiki

## Autores

- GUILHERME BASILIO SILVA FELIX XAVIER
- CATARINA ALVES BEZERRA
- DANTAS DE ARAUJO VALERIANO
- DANIEL HENRIQUE PINHEIRO LOPES DE SOUZA
- VICTOR MEDEIROS DE OLIVEIRA
- JOAO VICTOR DA SILVA PEIXOTO
