import re

def generate_html():
    with open("/Users/andresmartinez/Documents/GitHub/investigacioncienciadedatos/machine-learning.html", "r") as f:
        content = f.read()
    
    style_match = re.search(r'<style>.*?</style>', content, re.DOTALL)
    style = style_match.group(0) if style_match else '<style></style>'

    html = f"""<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sistemas Agroalimentarios | CIDEX</title>
    <link rel="stylesheet" href="styles.css" />
    {style}
</head>

<body>

    <section class="hero-linea">
        <div class="container">
            <a href="index.html#lineas" class="back-link">← Volver a líneas de investigación</a>

            <div class="hero-grid">
                <div>
                    <div class="eyebrow">Línea de investigación</div>
                    <h1>Sistemas Agroalimentarios</h1>
                    <p>
                        Esta línea se enfoca en el estudio, análisis y diseño de soluciones basadas en datos para
                        mejorar la sostenibilidad, eficiencia y equidad de las cadenas de valor agroalimentarias. 
                        Integra perspectivas jurídicas, económicas y matemáticas para abordar los retos del sector.
                    </p>

                    <div class="hero-tags">
                        <span>Sostenibilidad</span>
                        <span>Cadenas de valor</span>
                        <span>Políticas públicas</span>
                        <span>Seguridad alimentaria</span>
                    </div>
                </div>

                <div class="hero-card">
                    <h3>Qué busca esta línea</h3>
                    <p>
                        Desarrollar conocimiento interdisciplinario que conecte el marco regulatorio, el análisis 
                        de sistemas productivos y las herramientas cuantitativas para proponer estrategias 
                        innovadoras en sistemas agroalimentarios sostenibles.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="section-title">
                <div class="eyebrow">Propósito</div>
                <h2>Conectando tecnología, marco legal y sostenibilidad</h2>
                <p>
                    Construir un ecosistema de investigación que permita entender la complejidad de los 
                    sistemas agroalimentarios y formular propuestas que impacten positivamente el territorio.
                </p>
            </div>

            <div class="content-grid">
                <div class="content-card">
                    <p>
                        Esta línea articula visiones desde el derecho, la economía y la ingeniería para analizar 
                        los desafíos contemporáneos en la producción, distribución y consumo de alimentos. 
                    </p>
                    <p>
                        A través de análisis de datos e innovación, se fomenta la estructuración de cadenas 
                        de valor más resilientes, que consideren la regulación, el impacto ambiental y el 
                        desarrollo socioeconómico.
                    </p>
                </div>

                <div class="feature-list">
                    <div class="feature-card">
                        <h3>Sostenibilidad Agroalimentaria</h3>
                        <p>
                            Estrategias y modelos para promover prácticas agrícolas y alimentarias responsables 
                            y sostenibles a largo plazo.
                        </p>
                    </div>

                    <div class="feature-card">
                        <h3>Regulación y Políticas Públicas</h3>
                        <p>
                            Análisis del marco jurídico y diseño de políticas para la gobernanza y equidad 
                            en las cadenas productivas.
                        </p>
                    </div>

                    <div class="feature-card">
                        <h3>Analítica y Optimización</h3>
                        <p>
                            Uso de herramientas matemáticas y ciencia de datos para optimizar procesos 
                            agroindustriales y la gestión de recursos.
                        </p>
                    </div>

                    <div class="feature-card">
                        <h3>Desarrollo Territorial</h3>
                        <p>
                            Estudio de los impactos socioeconómicos y fortalecimiento de las capacidades 
                            en las regiones productoras.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section" style="padding-top: 0;">
        <div class="container">
            <div class="section-title">
                <div class="eyebrow">Profesores vinculados</div>
                <h2>Equipo académico de la línea</h2>
                <p>
                    La línea reúne profesores con trayectoria en derecho, análisis regional, matemáticas,
                    economía y sistemas agroalimentarios.
                </p>
            </div>

            <div class="professors-grid">

                <!-- PATRICIA -->
                <article class="prof-card">
                    <img src="profesores/guzman-aguilera-nidia-patricia.jpg" alt="Nidia Patricia Guzman Aguilera">
                    <div class="prof-content">
                        <h3>Nidia Patricia Guzman Aguilera</h3>
                        <div class="prof-role">Derecho y sistemas sostenibles</div>
                        <p>Abogada y administradora, magíster en análisis regional y Doctora (PhD) en Derecho.</p>
                        
                        <div class="prof-email">
                            <a href="mailto:patricia.guzman@uexternado.edu.co">patricia.guzman@uexternado.edu.co</a>
                        </div>
                        <div class="prof-links">
                            <a href="#" target="_blank">ORCID</a>
                            <a href="#" target="_blank">Scholar</a>
                            <a href="#" target="_blank">CvLAC</a>
                            <a href="#" target="_blank">Academia</a>
                            <a href="#" target="_blank">ResearchGate</a>
                        </div>
                        <div class="project-box">
                            <strong>Proyecto actual</strong>
                            <span>Sistemas agroalimentarios sostenibles</span>
                        </div>
                        <div class="prof-tags">
                            <span>Sistemas Agroalimentarios</span>
                        </div>
                    </div>
                </article>

                <!-- SANTIAGO -->
                <article class="prof-card">
                    <img src="profesores/perez-angarita-santiago.jpg" alt="Santiago Alejandro Perez Angarita">
                    <div class="prof-content">
                        <h3>Santiago Alejandro Perez Angarita</h3>
                        <div class="prof-role">Matemáticas y economía</div>
                        <p>Licenciado en Matemáticas y magíster en Economía. Estudiante de doctorado en Ingeniería.</p>
                        
                        <div class="prof-email">
                            <a href="mailto:santiago.perez@uexternado.edu.co">santiago.perez@uexternado.edu.co</a>
                        </div>
                        <div class="prof-links">
                            <a href="#" target="_blank">ORCID</a>
                            <a href="#" target="_blank">Scholar</a>
                            <a href="#" target="_blank">CvLAC</a>
                            <a href="#" target="_blank">Academia</a>
                            <a href="#" target="_blank">ResearchGate</a>
                        </div>
                        <div class="project-box">
                            <strong>Proyecto actual</strong>
                            <span>Estrategias de evaluación para la ciencia de datos</span>
                        </div>
                        <div class="prof-tags">
                            <span>Modelado Matemático</span>
                            <span>Sistemas Agroalimentarios</span>
                        </div>
                    </div>
                </article>

            </div>
        </div>
    </section>

    <div class="container footer-note">
        Para que las fotos carguen bien en GitHub Pages, usa nombres de archivo sin espacios y en minúsculas dentro de
        la carpeta <strong>profesores</strong>.
    </div>

</body>

</html>
"""

    with open("/Users/andresmartinez/Documents/GitHub/investigacioncienciadedatos/sistemas-agroalimentarios.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    generate_html()
