import re

html_file = "modelado-matematico.html"
files_to_search = ["machine-learning.html", "gestion-del-conocimiento.html", "sistemas-agroalimentarios.html", "index.html"]

# 1. Grab all prof-links from other pages and map them to their email domains
links_by_email = {}
for f in files_to_search:
    try:
        content = open(f).read()
    except FileNotFoundError:
        continue
    blocks = re.findall(r"(<div class=\"prof-email\".*?</a>\s*</div>\s*<div class=\"prof-links\">.*?</div>)", content, flags=re.DOTALL)
    for b in blocks:
        # extract email
        m_email = re.search(r"mailto:(.*?)\"", b)
        if m_email:
            email = m_email.group(1).strip()
            # extract links block
            m_links = re.search(r"(<div class=\"prof-links\">.*?</div>)", b, flags=re.DOTALL)
            if m_links:
                links_by_email[email] = m_links.group(1)

# Now, read target and apply
content = open(html_file).read()

def replacer(match):
    block = match.group(0)
    # determine email
    m_email = re.search(r"mailto:(.*?)\"", block)
    if not m_email:
        return block
    email = m_email.group(1).strip()
    
    if email in links_by_email and '<div class="prof-links">' not in block:
        # insert links block right after the prof-email block
        return block + "\n                        " + links_by_email[email]
    
    return block

# The regex to capture just the prof-email block (we will replace it with itself + the links)
new_content = re.sub(r'<div class="prof-email">.*?</div>', replacer, content, flags=re.DOTALL)

if new_content != content:
    open(html_file, "w").write(new_content)
    print("Patched links successfully.")
else:
    print("No changes made.")

# print which ones we missed
for m in re.finditer(r'<div class="prof-email">\s*<a href="mailto:(.*?)".*?</div>(.*?)(<div class="project-box">|<div class="prof-tags">)', new_content, flags=re.DOTALL):
    email = m.group(1)
    following_content = m.group(2)
    if '<div class="prof-links">' not in following_content:
        if email not in links_by_email:
            print("Missing links for email:", email, "- Not found in any other page.")
