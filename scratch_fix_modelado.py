import re

html_file = "modelado-matematico.html"
content = open(html_file).read()

# 1. Restore Color variables
content = content.replace("--green-dark: #0b3d2c;", "--theme-dark: #1e40af;")
content = content.replace("--green-main: #0f5a3c;", "--theme-main: #2563eb;")
content = content.replace("--green-soft: #eaf4ef;", "--theme-soft: #dbeafe;")

# Replace in styles using green variables to theme variables
content = content.replace("var(--green-main)", "var(--theme-main)")
content = content.replace("var(--green-dark)", "var(--theme-dark)")
content = content.replace("var(--green-soft)", "var(--theme-soft)")

# Hero linea
pattern = r'background:\s*linear-gradient\(135deg,\s*rgba\(15,\s*90,\s*60,\s*.*?\)[\s\S]*?\);'
replacement = 'background: linear-gradient(135deg, var(--theme-main), var(--theme-dark));'
content = re.sub(pattern, replacement, content)

open(html_file, "w").write(content)
print("Colors and hero fixed.")
