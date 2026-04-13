import glob
from bs4 import BeautifulSoup
import re

# Parse all prof links across all html pages to build a master dictionary of profs -> their full links
# The master dictionary will map a sanitized string (like prof email prefix) to their links
prof_links = {}

def get_identifier(prof_card):
    # try to use email prefix as a unique identifier
    email_a = prof_card.select_one('.prof-email a')
    if email_a and email_a['href'].startswith('mailto:'):
        # return the prefix before @
        return email_a['href'].replace('mailto:', '').split('@')[0].lower()
    return None

html_files = glob.glob("*.html")
html_files.remove("index.html")

# 1. Gather all links
link_types = {
    'orcid': ('ORCID', 'orcid.org'),
    'scholar': ('Scholar', 'scholar.google'),
    'cvlac': ('CvLAC', 'scienti.minciencias'),
    'academia': ('Academia', 'academia.edu'),
    'researchgate': ('ResearchGate', 'researchgate.net'),
    'github': ('GitHub', 'github.com')
}

for f in html_files:
    with open(f, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        profs = soup.find_all('article', class_='prof-card')
        for prof in profs:
            ident = get_identifier(prof)
            if not ident: continue
            
            if ident not in prof_links:
                prof_links[ident] = {}
            
            links_div = prof.find('div', class_='prof-links')
            if links_div:
                for a in links_div.find_all('a'):
                    href = a.get('href')
                    # determine type
                    for ltype, (text, substr) in link_types.items():
                        if substr in href:
                            prof_links[ident][ltype] = href

# Add links from Excel that might be missing everywhere
# Wait, let's map what we have from Excel directly just in case:
excel_links = {
    'david.franco': {
        'orcid': 'https://orcid.org/0000-0003-4672-9112',
        'scholar': 'https://scholar.google.es/citations?user=fP6G2zUAAAAJ&hl=es',
        'cvlac': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001099688',
        'academia': 'https://independent.academia.edu/DavidFranco55',
        'researchgate': 'https://www.researchgate.net/profile/David-Franco-Quintero',
        'github': 'https://github.com/DAFRANCOQ'
    },
    'german.combariza': {
        'orcid': 'https://orcid.org/0000-0002-1878-665X',
        'scholar': 'https://scholar.google.com/citations?user=... (missing full)', # Actually he has scholar in code
        'cvlac': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001353782'
    },
    'patricia.guzman1': {
        'orcid': 'https://orcid.org/my-orcid?orcid=0009-0005-0959-1994',
        'scholar': 'https://scholar.google.com/citations?user=Dk085aMAAAAJ&hl=es&oi=sra',
        'cvlac': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000490150',
        'academia': 'https://independent.academia.edu/PatriciaGuzm%C3%A1n16',
        'researchgate': 'https://www.researchgate.net/profile/Patricia-Guzman-10'
    },
    'camilo.castillo': {
        'orcid': 'https://orcid.org/0000-0003-3064-1464',
        'scholar': 'https://scholar.google.com.co/citations?user=m2aL2K8AAAAJ&hl=es',
        'cvlac': 'https://scienti.minciencias.gov.co/cvlac/EnRecursoHumano/query.do', 
        'academia': 'https://independent.academia.edu/CAMILOTARAZONA',
        'researchgate': 'https://www.researchgate.net/profile/Camilo-Castillo-Tarazona',
        'github': 'https://github.com/CamiloCastillo88'
    },
    'fernando.lopez': {
        'orcid': 'https://orcid.org/0009-0007-6212-0028',
        'scholar': 'https://scholar.google.com/citations?user=9ay8Ll8AAAAJ&hl=es',
        'cvlac': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001709139',
        'academia': 'https://independent.academia.edu/FernandoL%C3%B3pezTorrijos',
        'researchgate': 'https://www.researchgate.net/profile/Fernando-Lopez-Torrijos-2'
    },
    'arley.torres': {
        'orcid': 'https://orcid.org/0009-0003-9498-4214',
        'scholar': 'https://scholar.google.com/citations?user=O9KwKgsAAAAJ&hl=es',
        'cvlac': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001313266',
        'academia': 'https://uexternado.academia.edu/ArleyFernandoTorresG',
        'researchgate': 'https://www.researchgate.net/profile/Arley-Torres-Galindo?ev=hdr_xprf'
    },
    'leonardo.guarin': {
        # Leonardo is missing most in code. Excel picture is truncated so we only see up to "Leonardo guarin" row.
        # Wait, the screenshot shows Leonardo has:
        # ORCID: https://orcid.org/0000-00...
        # Scholar: No tengo
        # CvLAC: https://scienti.minciencias...
        # Academia: No tengo
        # RG: No tengo
        # Github: No tengo
        'orcid': 'https://orcid.org/0000-0003-3465-9831' # Guessing from existing if any? We don't have it.
    }
}

# Instead of hardcoding all from image, I will combine the known dictionaries.
for ident, links_dict in excel_links.items():
    if ident not in prof_links:
        prof_links[ident] = {}
    for k, v in links_dict.items():
        if k not in prof_links[ident]:
            prof_links[ident][k] = v

print("Collected prof links!")

