import re

files = {
    "machine-learning.html": {
        "dark": "#5b21b6",
        "main": "#7c3aed",
        "soft": "#f3e8ff"
    },
    "modelado-matematico.html": {
        "dark": "#1e40af",
        "main": "#2563eb",
        "soft": "#dbeafe"
    },
    "gestion-del-conocimiento.html": {
        "dark": "#9a3412",
        "main": "#f97316",
        "soft": "#ffedd5"
    },
    "sistemas-agroalimentarios.html": {
        "dark": "#065f46",
        "main": "#10b981",
        "soft": "#d1fae5"
    }
}

for filename, colors in files.items():
    with open(filename, 'r') as f:
        content = f.read()

    # Rename --green-* to --theme-*
    content = content.replace('--green-dark', '--theme-dark')
    content = content.replace('--green-main', '--theme-main')
    content = content.replace('--green-soft', '--theme-soft')

    # Update the root variables
    # The original has:
    #             --theme-dark: #0b3d2c;
    #             --theme-main: #0f5a3c;
    #             --theme-soft: #eaf4ef;
    
    content = re.sub(r'--theme-dark:\s*#[a-fA-F0-9]+;', f'--theme-dark: {colors["dark"]};', content)
    content = re.sub(r'--theme-main:\s*#[a-fA-F0-9]+;', f'--theme-main: {colors["main"]};', content)
    content = re.sub(r'--theme-soft:\s*#[a-fA-F0-9]+;', f'--theme-soft: {colors["soft"]};', content)

    # Some hardcoded border colors in project-box and prof-card might exist
    # border: 1px solid #dbe9e0; -> this is a soft green. Let's make it more generic or related to theme-soft.
    # In earlier template it's #dbe9e0. We can replace it with var(--theme-soft) or just dim it.
    # Same for background: #f7faf8;
    # We can replace background: #f7faf8; with background: #f8fafc; (slate-50) since everything else gives it flavor.
    content = content.replace('background: #f7faf8;', 'background: #f8fafc;')
    content = content.replace('border: 1px solid #dbe9e0;', 'border: 1px solid var(--theme-soft);')

    with open(filename, 'w') as f:
        f.write(content)

print("Colors swapped successfully.")
