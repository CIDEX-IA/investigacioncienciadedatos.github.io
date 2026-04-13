import re
import glob
from bs4 import BeautifulSoup

expected = ['mailto', 'orcid.org', 'scholar.google', 'scienti.minciencias', 'academia', 'researchgate', 'github']

html_files = glob.glob("*.html")
for f in html_files:
    if "index" in f: continue
    print(f)
    print(f"\n--- {f} ---")
    with open(f, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        profs = soup.find_all('article', class_='prof-card')
        for prof in profs:
            name_tag = prof.find('h3')
            name = name_tag.text.strip() if name_tag else "Unknown"
            links = [a['href'] for a in prof.find_all('a', href=True)]
            found = []
            for e in expected:
                if any(e in l for l in links):
                    found.append(e)
            missing = [e for e in expected if e not in found]
            print(f"- {name}: Missing -> {missing}")
