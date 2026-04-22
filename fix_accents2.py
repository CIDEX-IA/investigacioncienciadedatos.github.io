import os
import re

replacements = {
    # Names
    r'\bAndres\b': 'Andrés',
    r'\bJose\b': 'José',
    r'\bJulian\b': 'Julián',
    r'\bGerman\b': 'Germán',
    r'\bAngelica\b': 'Angélica',
    r'\bMartinez\b': 'Martínez',
    r'\bLopez\b': 'López',
    r'\bPerez\b': 'Pérez',
    r'\bDiaz\b': 'Díaz',
    r'\bSanchez\b': 'Sánchez',
    r'\bGomez\b': 'Gómez',
    r'\bGonzalez\b': 'González',
    r'\bFlorez\b': 'Flórez',
    r'\bHernandez\b': 'Hernández',
    r'\bGarcia\b': 'García',
    
    # Nouns & common words
    r'\binvestigacion\b': 'investigación',
    r'\binvestigaciones\b': 'investigaciones', # no change, but covers plural if needed
    r'\bInvestigacion\b': 'Investigación',
    r'\bgestion\b': 'gestión',
    r'\bGestion\b': 'Gestión',
    r'\btecnologia\b': 'tecnología',
    r'\btecnologias\b': 'tecnologías',
    r'\bTecnologia\b': 'Tecnología',
    r'\bmatematico\b': 'matemático',
    r'\bmatematicos\b': 'matemáticos',
    r'\bMatematico\b': 'Matemático',
    r'\bmatematica\b': 'matemática',
    r'\bmatematicas\b': 'matemáticas',
    r'\bMatematica\b': 'Matemática',
    r'\bMatematicas\b': 'Matemáticas',
    r'\bestadistica\b': 'estadística',
    r'\bEstadistica\b': 'Estadística',
    r'\binformacion\b': 'información',
    r'\bInformacion\b': 'Información',
    r'\bcomunicacion\b': 'comunicación',
    r'\bComunicacion\b': 'Comunicación',
    r'\banalisis\b': 'análisis',
    r'\bAnalisis\b': 'Análisis',
    r'\boptimizacion\b': 'optimización',
    r'\bOptimizacion\b': 'Optimización',
    r'\bmetodos\b': 'métodos',
    r'\bMetodos\b': 'Métodos',
    r'\bevaluacion\b': 'evaluación',
    r'\bEvaluacion\b': 'Evaluación',
    r'\bresolucion\b': 'resolución',
    r'\bResolucion\b': 'Resolución',
    r'\bintroduccion\b': 'introducción',
    r'\bIntroduccion\b': 'Introducción',
    r'\bsolucion\b': 'solución',
    r'\bSolucion\b': 'Solución',
    r'\bproposito\b': 'propósito',
    r'\bProposito\b': 'Propósito',
    r'\bexito\b': 'éxito',
    r'\bExito\b': 'Éxito',
    r'\bdinamica\b': 'dinámica',
    r'\bDinamica\b': 'Dinámica',
    r'\bgeografico\b': 'geográfico',
    r'\bGeografico\b': 'Geográfico',
    r'\beconomico\b': 'económico',
    r'\bEconomico\b': 'Económico',
    r'\bbasico\b': 'básico',
    r'\bBasico\b': 'Básico',
    r'\btecnicas\b': 'técnicas',
    r'\bTecnicas\b': 'Técnicas',
    r'\bextencion\b': 'extensión', 
    r'\bExtencion\b': 'Extensión', 
    r'\bpractica\b': 'práctica',
    r'\bPractica\b': 'Práctica',
    r'\baplicacion\b': 'aplicación',
    r'\bAplicacion\b': 'Aplicación',
    r'\bultimo\b': 'último',
    r'\bUltimo\b': 'Último',
    
    # Specific ones
    r'\bImagenes\b': 'Imágenes',
    r'\bautomatico\b': 'automático',
    r'\bAutomatica\b': 'Automática',
    r'\bautomatica\b': 'automática',
    r'\bAlgoritmico\b': 'Algorítmico',
    r'\balgoritmico\b': 'algorítmico',
    r'\bCiencias\b': 'Ciencias',
    r'\bagricola\b': 'agrícola',
    r'\bAgricola\b': 'Agrícola',
    r'\btambien\b': 'también',
    r'\bTambien\b': 'También',
    r'\bmas\b': 'más',
    r'\bMas\b': 'Más'
}

def replace_in_text(text):
    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)
    return text

files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('<!')]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False
    
    # Split the file by tags. Odd indices will be tags, even indices will be text.
    parts = re.split(r'(<[^>]+>)', content)
    
    for i in range(len(parts)):
        if i % 2 == 0:
            # It's text, safe to replace
            new_text = replace_in_text(parts[i])
            # BUT wait, "mas" -> "más" is dangerous, e.g. "Tomas". Wait, \bmas\b works.
            # But the 'html' file might have javascript or inline CSS logic. Unlikely to use "mas".
            if parts[i] != new_text:
                parts[i] = new_text
                modified = True
        else:
            # It's a tag. We should replace alt="..." and title="..." values carefully.
            tag = parts[i]
            # Find all alt="..." or title="..."
            for attr in ['alt', 'title']:
                attr_pattern = re.compile(rf'{attr}="([^"]+)"')
                def attr_repl_func(m):
                    return f'{attr}="{replace_in_text(m.group(1))}"'
                new_tag = attr_pattern.sub(attr_repl_func, tag)
                if new_tag != tag:
                    tag = new_tag
                    modified = True
            parts[i] = tag
            
    if modified:
        new_content = "".join(parts)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Updated {f}")
