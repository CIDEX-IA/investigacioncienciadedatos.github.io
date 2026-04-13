import re
import os

files = [
    "gestion-del-conocimiento.html",
    "machine-learning.html",
    "modelado-matematico.html",
    "sistemas-agroalimentarios.html"
]

data = {
    "german.combariza": {
        "semillero": "Teoría de Grafos",
        "proyecto": "Proyectos de Investigación UExternado"
    },
    "lopez-torrijos-fernando": {
        "semillero": "No especificado",
        "proyecto": "Grupo de investigación en Procesamiento de Imágenes"
    },
    # we use an anchor in their block
    "alber.montenegro@uexternado|montenegro-vargas": {
        "semillero": "No especificado",
        "proyecto": "RestANNs"
    },
    "juan.uruena1@": {
        "semillero": "Aprendizaje Reforzado",
        "proyecto": "Vulnerability Index"
    },
    "jose.tapias1@": {
        "semillero": "Semillero ILomugo",
        "proyecto": "Investigación proyecto Clínica de Occidente, índice de vulnerabilidad"
    },
    "julian.sanchez@": {
        "semillero": "Aprendizaje Reforzado",
        "proyecto": "Evaluación de estudiantes y Vulnerability Index"
    }
}

for f in files:
    if not os.path.exists(f): continue
    content = open(f).read()
    
    # We will match the entire block from <div class="prof-content"> up to <div class="prof-tags">
    # and re-write the project-box part inside.
    
    def replacer(match):
        block = match.group(0)
        
        # Determine which professor this block belongs to
        prof_key = None
        for k in data.keys():
            if re.search(k, block, re.IGNORECASE):
                prof_key = k
                break
                
        if not prof_key:
            return block # no change
            
        # extract current structure by removing any existing project-boxes completely
        cleaned_block = re.sub(r'<div class="project-box">.*?</div>', '', block, flags=re.DOTALL)
        
        # build the new boxes
        d = data[prof_key]
        
        boxes = f"""<div class="project-box">
                            <strong>Semillero</strong>
                            <span>{d["semillero"]}</span>
                        </div>
                        <div class="project-box">
                            <strong>Proyecto actual</strong>
                            <span>{d["proyecto"]}</span>
                        </div>
                        <div class="prof-tags">"""
                        
        # Now append them exactly where prof-tags was
        final_block = cleaned_block.replace('<div class="prof-tags">', boxes)
        
        # fix any excessive newlines created by removing previous boxes
        final_block = re.sub(r'\n\s*\n\s*\n', '\n\n', final_block)
        
        return final_block

    new_content = re.sub(r'<div class="prof-content">.*?<div class="prof-tags">', replacer, content, flags=re.DOTALL)
    
    if new_content != content:
        open(f, "w").write(new_content)
        print("Updated double boxes in", f)

print("Done")
