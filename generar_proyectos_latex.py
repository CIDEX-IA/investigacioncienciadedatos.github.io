
import os
import re
import math
import glob
import pandas as pd
from pathlib import Path

# =========================================================
# Configuración
# =========================================================
# Puedes fijar una ruta exacta o dejar None para autodetectar el Excel.
EXCEL_PATH = None
SHEET_NAME = 0
OUTPUT_DIR = "latex_proyectos"
LOGO_FILE = "firma.jpg"   # opcional; si no existe, el documento compila sin logo

# =========================================================
# Utilidades
# =========================================================
def find_excel_file():
    if EXCEL_PATH:
        p = Path(EXCEL_PATH)
        if p.exists():
            return p
    candidates = list(Path(".").glob("*.xlsx"))
    if len(candidates) == 1:
        return candidates[0]
    # prioriza archivos cuyo nombre contenga "proyecto"
    prioritized = [c for c in candidates if "proyecto" in c.name.lower()]
    if len(prioritized) == 1:
        return prioritized[0]
    if not candidates:
        raise FileNotFoundError("No se encontró ningún archivo .xlsx en la carpeta actual.")
    raise FileNotFoundError(
        "Hay varios archivos .xlsx en la carpeta actual. "
        "Define la variable EXCEL_PATH con el nombre exacto del archivo que deseas usar."
    )

def is_missing(value):
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    txt = str(value).strip()
    return txt == "" or txt.lower() in {"nan", "none", "na", "n/a"}

def clean_text(value):
    if is_missing(value):
        return ""
    txt = str(value).strip()
    txt = re.sub(r"\s+", " ", txt)
    return txt

def latex_escape(text):
    if is_missing(text):
        return ""
    text = str(text)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def split_items(value):
    txt = clean_text(value)
    if not txt:
        return []
    parts = re.split(r";|\n", txt)
    return [p.strip() for p in parts if p.strip() and p.strip().lower() != "ninguno"]

def bullet_list(items):
    items = [latex_escape(clean_text(x)) for x in items if clean_text(x)]
    if not items:
        return "No reportado."
    body = "\n".join([rf"    \item {item}" for item in items])
    return "\\begin{itemize}\n" + body + "\n\\end{itemize}"

def paragraph_or_default(value, default="No reportado."):
    txt = clean_text(value)
    if not txt:
        return default
    return latex_escape(txt)

def format_date(value):
    if is_missing(value):
        return "No reportado"
    try:
        dt = pd.to_datetime(value)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return latex_escape(str(value))

def safe_filename(text, max_len=90):
    text = clean_text(text).lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[-\s]+", "_", text).strip("_")
    return text[:max_len] if text else "proyecto"

# =========================================================
# Plantilla LaTeX
# =========================================================
def render_project_tex(row):
    titulo = paragraph_or_default(row.get("Título del Proyecto"))
    principal = paragraph_or_default(row.get("Nombre Completo Investigador Principal"))
    coinvestigadores = split_items(row.get("Nombre de Co-investigadores que pertenecen al grupo, separados por coma (Nombre Apellido, Nombre Apellido)"))
    lineas = split_items(row.get("Lineas de Investigación a las que se articula el proyecto"))
    aliados = split_items(row.get("Aliados externos"))
    comunidad_ext = split_items(row.get("Comunidades Externas a las que se espera impactar"))
    comunidad_int = split_items(row.get("Comunidades Internas a las que se espera impactar"))
    participacion_semillero = split_items(row.get("Tipo de participación del semillero\xa0"))
    req_tecnologicos = split_items(row.get("Requerimientos tecnológicos"))
    resultados_cientificos = split_items(row.get("Resultados esperados Científicos"))
    productos_aplicados = split_items(row.get("Productos aplicados"))

    anio_inicio = format_date(row.get("Año de Inicio"))
    duracion = paragraph_or_default(row.get("Duración estimada en meses ( NA si no aplica)"))
    estado = paragraph_or_default(row.get("Estado del Proyecto"))
    tiene_semillero = paragraph_or_default(row.get("Tiene Vinculado un Semillero"))
    nombre_semillero = paragraph_or_default(row.get("Nombre del Semillero"), default="No aplica")
    tipo_proyecto = paragraph_or_default(row.get("Tipo de proyecto"))
    nivel_avance = paragraph_or_default(row.get("Nivel de avance actual"))
    financiacion = paragraph_or_default(row.get("Posibles fuentes de financiación\n"))

    problema = paragraph_or_default(row.get("Problema de investigación"))
    objetivo = paragraph_or_default(row.get("Objetivo general"))
    metodologia = paragraph_or_default(row.get("Basado en lo anterior describa la metodología"))
    resultados_generales = paragraph_or_default(row.get("Enuncie los resultados generales esperados del proyecto"))

    latex = rf"""
\documentclass[a4paper,12pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[spanish]{{babel}}
\usepackage{{geometry}}
\usepackage{{graphicx}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}
\usepackage{{fancyhdr}}
\usepackage{{enumitem}}
\usepackage{{amsmath}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{setspace}}
\usepackage{{float}}
\usepackage{{longtable}}
\usepackage{{tabularx}}
\usepackage{{ragged2e}}

\geometry{{top=34mm,bottom=25mm,left=25mm,right=25mm}}

\definecolor{{ExternadoGreen}}{{RGB}}{{0,104,55}}
\definecolor{{ExternadoDark}}{{RGB}}{{0,51,25}}
\definecolor{{ExternadoGold}}{{RGB}}{{198,146,20}}

\hypersetup{{colorlinks=true,linkcolor=ExternadoGreen,urlcolor=ExternadoGreen,citecolor=ExternadoGreen}}

\setlength{{\headheight}}{{52pt}}
\pagestyle{{fancy}}
\fancyhf{{}}
\fancyhead[L]{{\IfFileExists{{{latex_escape(LOGO_FILE)}}}{{\includegraphics[height=40pt]{{{latex_escape(LOGO_FILE)}}}}}{{}}}}
\fancyhead[R]{{\textcolor{{ExternadoGreen}}{{\small Departamento de Matemáticas}}}}
\fancyfoot[C]{{\textcolor{{ExternadoDark}}{{\thepage}}}}

\fancypagestyle{{plain}}{{
  \fancyhf{{}}
  \fancyhead[L]{{\IfFileExists{{{latex_escape(LOGO_FILE)}}}{{\includegraphics[height=40pt]{{{latex_escape(LOGO_FILE)}}}}}{{}}}}
  \fancyhead[R]{{\textcolor{{ExternadoGreen}}{{\small Universidad Externado de Colombia}}}}
  \fancyfoot[C]{{\textcolor{{ExternadoDark}}{{\thepage}}}}
}}

\title{{
\vspace{{-8mm}}
\textbf{{\textcolor{{ExternadoGreen}}{{Ficha de Proyecto de Investigación}}}}\\
\large \textcolor{{ExternadoDark}}{{Grupo de Investigación en Ciencia de Datos}}\\
\large \textcolor{{ExternadoDark}}{{Universidad Externado de Colombia}}
}}
\author{{\textcolor{{ExternadoDark}}{{Departamento de Matemáticas}}}}
\date{{\textcolor{{ExternadoDark}}{{\today}}}}

\setlist[itemize]{{leftmargin=*, itemsep=3pt, topsep=3pt}}
\setstretch{{1.12}}

\begin{{document}}
\maketitle
\vspace{{-3mm}}
\noindent\textcolor{{ExternadoDark}}{{\rule{{\textwidth}}{{0.6pt}}}}

\section*{{1. Información general}}
\begin{{longtable}}{{p{{4.2cm}} p{{10.4cm}}}}
\toprule
\textbf{{Campo}} & \textbf{{Detalle}} \\
\midrule
Título del proyecto & {titulo} \\
Investigador principal & {principal} \\
Co-investigadores & {paragraph_or_default(", ".join(coinvestigadores), default="No reportado")} \\
Líneas de investigación & {paragraph_or_default(", ".join(lineas), default="No reportado")} \\
Año de inicio & {anio_inicio} \\
Duración estimada & {duracion} \\
Estado del proyecto & {estado} \\
Tipo de proyecto & {tipo_proyecto} \\
Nivel de avance actual & {nivel_avance} \\
Semillero vinculado & {tiene_semillero} \\
Nombre del semillero & {nombre_semillero} \\
Fuentes de financiación & {financiacion} \\
\bottomrule
\end{{longtable}}

\section*{{2. Problema de investigación}}
{problema}

\section*{{3. Objetivo general}}
{objetivo}

\section*{{4. Metodología}}
{metodologia}

\section*{{5. Comunidades a impactar}}
\subsection*{{5.1. Comunidades externas}}
{bullet_list(comunidad_ext)}

\subsection*{{5.2. Comunidades internas}}
{bullet_list(comunidad_int)}

\section*{{6. Semillero y articulación formativa}}
\subsection*{{6.1. Participación del semillero}}
{bullet_list(participacion_semillero)}

\subsection*{{6.2. Aliados externos}}
{bullet_list(aliados)}

\section*{{7. Requerimientos tecnológicos}}
{bullet_list(req_tecnologicos)}

\section*{{8. Resultados esperados}}
\subsection*{{8.1. Resultados generales}}
{resultados_generales}

\subsection*{{8.2. Resultados científicos esperados}}
{bullet_list(resultados_cientificos)}

\subsection*{{8.3. Productos aplicados}}
{bullet_list(productos_aplicados)}

\section*{{9. Observación de gestión}}
Este documento fue generado automáticamente a partir del formulario de registro de proyectos del grupo. Se recomienda revisar y ajustar la redacción final antes de su circulación institucional o envío a convocatorias.

\end{{document}}
"""
    return latex.strip() + "\n"

def main():
    excel_path = find_excel_file()
    df = pd.read_excel(excel_path, sheet_name=SHEET_NAME)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    for _, row in df.iterrows():
        titulo = clean_text(row.get("Título del Proyecto")) or "Proyecto"
        project_id = clean_text(row.get("ID"))
        fname = safe_filename(f"{project_id}_{titulo}") + ".tex"
        tex = render_project_tex(row)
        out_path = output_dir / fname
        out_path.write_text(tex, encoding="utf-8")
        generated.append(out_path.name)

    print(f"Excel usado: {excel_path.name}")
    print(f"Se generaron {len(generated)} archivos .tex en: {output_dir.resolve()}")
    for name in generated:
        print(" -", name)

if __name__ == "__main__":
    main()
