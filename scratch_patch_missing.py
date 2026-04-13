import re

html_file = "modelado-matematico.html"
content = open(html_file).read()

placeholder_links = """<div class="prof-links">
                            <a href="#" target="_blank">ORCID</a>
                            <a href="#" target="_blank">Scholar</a>
                            <a href="#" target="_blank">CvLAC</a>
                        </div>"""

def replacer(match):
    block = match.group(0)
    # determine email
    m_email = re.search(r"mailto:(.*?)\"", block)
    if not m_email:
        return block
    email = m_email.group(1).strip()
    
    if email in ["leonardo.guarin@uexternado.edu.co", "juan.uruena1@uexternado.edu.co"]:
        if '<div class="prof-links">' not in block:
            return block + "\n                        " + placeholder_links
    
    return block

new_content = re.sub(r'<div class="prof-email">.*?</div>', replacer, content, flags=re.DOTALL)

if new_content != content:
    open(html_file, "w").write(new_content)
    print("Patched missing placeholders.")
else:
    print("No changes.")
