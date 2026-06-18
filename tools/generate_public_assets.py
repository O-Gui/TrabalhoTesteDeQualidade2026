from html import escape
from pathlib import Path
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAGES_URL = "https://o-gui.github.io/TrabalhoTesteDeQualidade2026/"

sys.path.insert(0, str(ROOT))

from care_on_live_app import MEDICAMENTOS, PACIENTES, PROFISSIONAIS, SERVICOS, USUARIOS  # noqa: E402


def write_file(name: str, content: str) -> None:
    (DOCS / name).write_text(content, encoding="utf-8")


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)} - Care on Live</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header>
    <a class="brand" href="index.html">
      <span class="brand-mark">CL</span>
      <span><strong>Care on Live</strong><small>GitHub Pages</small></span>
    </a>
    <nav>
      <a href="index.html">Home</a>
      <a href="profissionais.html">Marketplace</a>
      <a href="medicamentos.html">Medicamentos</a>
      <a href="links.html">Links</a>
    </nav>
  </header>
  <main>
    {body}
  </main>
</body>
</html>
"""


def table(headers: list[str], rows: list[list[object]]) -> str:
    head = "".join(f"<th>{escape(str(header))}</th>" for header in headers)
    body = "\n".join(
        "<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f"""<table>
  <thead><tr>{head}</tr></thead>
  <tbody>{body}</tbody>
</table>"""


def card_grid(items: list[tuple[str, str, str]]) -> str:
    return '<section class="grid">' + "\n".join(
        f"""<article class="card">
  <h2>{escape(title)}</h2>
  <p>{escape(text)}</p>
  <a class="button" href="{escape(url)}">Abrir</a>
</article>"""
        for title, text, url in items
    ) + "</section>"


def generate_site() -> None:
    DOCS.mkdir(exist_ok=True)

    write_file(
        "styles.css",
        """*{box-sizing:border-box}body{margin:0;background:#f4f7f8;color:#172126;font-family:Arial,Helvetica,sans-serif;letter-spacing:0}header{background:#fff;border-bottom:1px solid #d7e2e2;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px max(16px,calc((100vw - 1180px)/2));position:sticky;top:0}main{width:min(1180px,calc(100% - 32px));margin:24px auto 48px}.brand{display:flex;align-items:center;gap:12px;color:#172126;text-decoration:none}.brand-mark{width:38px;height:38px;border-radius:8px;background:#087f8c;color:#fff;display:grid;place-items:center;font-weight:700}.brand strong,.brand small{display:block}.brand small{color:#65747b;margin-top:2px}nav{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}nav a,.button{border:1px solid #d7e2e2;border-radius:8px;background:#fff;color:#172126;display:inline-flex;align-items:center;min-height:38px;padding:9px 12px;text-decoration:none}.button{background:#087f8c;color:#fff;border-color:#087f8c;font-weight:700}.hero,.panel,.card{background:#fff;border:1px solid #d7e2e2;border-radius:8px}.hero,.panel{padding:20px}.hero h1{margin:0 0 8px;font-size:30px}.muted,p{color:#65747b}.grid,.marketplace{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:16px}.marketplace{grid-template-columns:repeat(4,minmax(0,1fr))}.card{padding:16px}.professional-card{display:grid;gap:12px;min-height:280px}.avatar{width:56px;height:56px;border-radius:8px;background:#eef5f3;color:#05626d;display:grid;place-items:center;font-size:20px;font-weight:700}.rating{color:#996f00;font-weight:700}.price{color:#05626d;font-size:18px;font-weight:700}.message{min-height:24px;color:#087443;font-weight:700}.card h2,.panel h2{margin:0 0 8px;font-size:20px}table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #d7e2e2;border-radius:8px;overflow:hidden}th,td{padding:12px;border-bottom:1px solid #d7e2e2;text-align:left;vertical-align:top}th{background:#eef5f3;color:#65747b;font-size:12px;text-transform:uppercase}.links{display:grid;gap:10px}.links a{background:#fff;border:1px solid #d7e2e2;border-radius:8px;padding:12px;color:#087f8c;text-decoration:none;font-weight:700}@media(max-width:820px){header{align-items:flex-start;flex-direction:column}.grid,.marketplace{grid-template-columns:1fr}table{display:block;overflow-x:auto;white-space:nowrap}}""",
    )
    write_file(".nojekyll", "")

    write_file(
        "index.html",
        page(
            "Inicio",
            f"""<section class="hero">
  <h1>Care on Live</h1>
  <p>Versao estatica para GitHub Pages com marketplace de profissionais, pacientes demonstrativos e links separados por area.</p>
  <a class="button" href="profissionais.html">Abrir marketplace</a>
</section>
{card_grid([
    ("Marketplace", "Escolha entre cuidadores, enfermeiros e fisioterapeutas ficticios.", "profissionais.html"),
    ("Medicamentos", "Rotinas ficticias de medicacao.", "medicamentos.html"),
    ("Links separados", "Todos os links principais da entrega.", "links.html"),
    ("Repositorio", "Codigo-fonte e documentacao tecnica do projeto.", "https://github.com/O-Gui/TrabalhoTesteDeQualidade2026"),
    ("Wiki", "Plano de qualidade e documentos da atividade.", "https://github.com/O-Gui/TrabalhoTesteDeQualidade2026/wiki"),
])}""",
        ),
    )

    write_file(
        "admin.html",
        page(
            "Admin",
            f"""<section class="hero">
  <h1>Painel do administrador</h1>
  <p>Resumo publico sem credenciais expostas na tela.</p>
</section>
<section class="grid">
  <article class="card"><h2>{len(PACIENTES)}</h2><p>Pacientes demonstrativos</p></article>
  <article class="card"><h2>{len(PROFISSIONAIS)}</h2><p>Profissionais ficticios</p></article>
  <article class="card"><h2>{len(SERVICOS)}</h2><p>Servicos publicados</p></article>
</section>
<section class="panel" style="margin-top:16px">
  <h2>Pacientes por risco</h2>
  {table(["Nome", "Idade", "Cuidador", "Risco", "Status"], [[p["nome"], p["idade"], p["cuidador"], p["risco"], p["status"]] for p in PACIENTES])}
</section>""",
        ),
    )

    write_file(
        "profissionais.html",
        page(
            "Marketplace de Profissionais",
            f"""<section class="hero">
  <h1>Marketplace de profissionais</h1>
  <p>Escolha um profissional ficticio para simular a contratacao do cuidado domiciliar.</p>
  <p id="selecionado" class="message"></p>
</section>
<section class="marketplace">
  {''.join(f'''<article class="card professional-card">
    <div class="avatar">{escape(p["nome"][0])}</div>
    <div><h2>{escape(p["nome"])}</h2><p>{escape(p["especialidade"])} - {escape(p["cidade"])}</p></div>
    <p>{escape(p["resumo"])}</p>
    <div><div class="rating">Nota {p["avaliacao"]:.1f}/5</div><div class="price">R$ {p["precoTurno"]:.2f} por turno</div><p>{escape(p["turno"])} - {escape(p["status"])}</p></div>
    <button class="button" onclick="selecionar('{escape(p["nome"])}')">Selecionar</button>
  </article>''' for p in PROFISSIONAIS)}
</section>
<script>
function selecionar(nome) {{
  document.getElementById('selecionado').innerText = 'Profissional selecionado: ' + nome;
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}
</script>""",
        ),
    )

    write_file(
        "pacientes.html",
        page(
            "Pacientes",
            f"""<section class="hero">
  <h1>Pacientes</h1>
  <p>Pacientes ficticios para demonstrar acompanhamento e risco.</p>
</section>
<section class="panel" style="margin-top:16px">
  {table(["Nome", "Idade", "Necessidade", "Cuidador", "Risco", "Status"], [[p["nome"], p["idade"], p["necessidadePrincipal"], p["cuidador"], p["risco"], p["status"]] for p in PACIENTES])}
</section>""",
        ),
    )

    write_file(
        "familiar.html",
        page(
            "Familiar",
            """<section class="hero">
  <h1>Painel do familiar</h1>
  <p>Visao estatica para acompanhamento remoto do cuidado.</p>
</section>
<section class="grid">
  <article class="card"><h2>Maria de Lourdes</h2><p>Paciente em acompanhamento domiciliar.</p></article>
  <article class="card"><h2>Cuidador</h2><p>Ana Paula Ribeiro no turno noturno.</p></article>
  <article class="card"><h2>Alertas</h2><p>Rotinas de medicamento e SOS acompanhadas.</p></article>
</section>""",
        ),
    )

    write_file(
        "medicamentos.html",
        page(
            "Medicamentos",
            f"""<section class="hero">
  <h1>Medicamentos</h1>
  <p>Rotinas ficticias de medicamentos por paciente.</p>
</section>
<section class="panel" style="margin-top:16px">
  {table(["Paciente", "Medicamento", "Horario", "Quantidade", "Status"], [[m["paciente"], m["nomeRemedio"], m["horarioRemedio"], m["quantidadeRemedio"], m["status"]] for m in MEDICAMENTOS])}
</section>""",
        ),
    )

    write_file(
        "links.html",
        page(
            "Links",
            f"""<section class="hero">
  <h1>Links separados</h1>
  <p>Use estes links na apresentacao ou na entrega via GitHub Pages.</p>
</section>
<section class="links" style="margin-top:16px">
  <a href="{PAGES_URL}">GitHub Pages - inicio</a>
  <a href="{PAGES_URL}profissionais.html">Marketplace de profissionais</a>
  <a href="{PAGES_URL}medicamentos.html">Medicamentos</a>
  <a href="{PAGES_URL}acessos-care-on-live.pdf">PDF de acessos</a>
  <a href="https://github.com/O-Gui/TrabalhoTesteDeQualidade2026">Repositorio GitHub</a>
  <a href="https://github.com/O-Gui/TrabalhoTesteDeQualidade2026/wiki">Wiki do projeto</a>
</section>""",
        ),
    )


def generate_pdf() -> None:
    pdf_path = DOCS / "acessos-care-on-live.pdf"
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=landscape(A4),
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
    )
    story = [
        Paragraph("Care on Live - Acessos de demonstracao", styles["Title"]),
        Paragraph(
            "Este PDF separa os usuarios de demonstracao para que emails e senhas nao fiquem expostos nas telas publicas.",
            styles["BodyText"],
        ),
        Spacer(1, 0.4 * cm),
    ]

    cell_style = styles["BodyText"]
    cell_style.fontSize = 7
    rows = [[Paragraph(item, cell_style) for item in ["Perfil", "Nome", "Email", "Senha", "Tela"]]]
    for email, usuario in USUARIOS.items():
        rows.append(
            [
                Paragraph(usuario["perfil"], cell_style),
                Paragraph(usuario["nome"], cell_style),
                Paragraph(email, cell_style),
                Paragraph(usuario["senha"], cell_style),
                Paragraph(f"{PAGES_URL}{usuario['dashboard'].strip('/')}.html", cell_style),
            ]
        )

    table_obj = Table(rows, colWidths=[3.0 * cm, 5.0 * cm, 5.2 * cm, 3.2 * cm, 9.0 * cm])
    table_obj.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#087f8c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d7e2e2")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef5f3")]),
            ]
        )
    )
    story.extend([table_obj, Spacer(1, 0.5 * cm)])
    story.append(Paragraph(f"GitHub Pages: {PAGES_URL}", styles["BodyText"]))
    story.append(Paragraph("Repositorio: https://github.com/O-Gui/TrabalhoTesteDeQualidade2026", styles["BodyText"]))
    doc.build(story)


def main() -> None:
    generate_site()
    generate_pdf()
    print(f"Arquivos gerados em {DOCS}")


if __name__ == "__main__":
    main()
