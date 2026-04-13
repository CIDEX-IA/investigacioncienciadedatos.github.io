import re

files = [
    "gestion-del-conocimiento.html",
    "machine-learning.html",
    "modelado-matematico.html",
    "sistemas-agroalimentarios.html"
]

for f in files:
    content = open(f).read()
    
    # Target replacement for background of hero-linea
    # We replace:
    # background:\n                linear-gradient(135deg, rgba(15, 90, 60, 0.96), rgba(11, 61, 44, 0.94));
    # with:
    # background: linear-gradient(135deg, var(--theme-main), var(--theme-dark));
    
    # using regex to catch any spacing
    pattern = r'background:\s*linear-gradient\(135deg,\s*rgba\(15,\s*90,\s*60,\s*.*?\)[\s\S]*?\);'
    replacement = 'background: linear-gradient(135deg, var(--theme-main), var(--theme-dark));'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        open(f, "w").write(new_content)
        print("Fixed hero background in", f)

print("Done")
