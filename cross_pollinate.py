import glob
from bs4 import BeautifulSoup
import re

html_files = glob.glob("*.html")
html_files.remove("index.html")

prof_links = {}

def get_identifier(prof_card):
    email_a = prof_card.select_one('.prof-email a')
    if email_a and email_a['href'].startswith('mailto:'):
        return email_a['href'].replace('mailto:', '').split('@')[0].lower()
    return None

link_types = {
    'ORCID': 'orcid.org',
    'Scholar': 'scholar.google',
    'CvLAC': 'scienti.minciencias',
    'Academia': 'academia.edu',
    'ResearchGate': 'researchgate.net',
    'GitHub': 'github.com'
}

# 1. Gather
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
                    for name, substr in link_types.items():
                        if substr in href:
                            prof_links[ident][name] = href

# 2. Update Patricia from what I can see in the image to be safe
prof_links['patricia.guzman1'] = {
    'ORCID': 'https://orcid.org/my-orcid?orcid=0009-0005-0959-1994',
    'Scholar': 'https://scholar.google.com/citations?user=Dk085aMAAAAJ&hl=es',
    'CvLAC': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000490150',
    'Academia': 'https://independent.academia.edu/PatriciaGuzm%C3%A1n16',
    'ResearchGate': 'https://www.researchgate.net/profile/Patricia-Guzman-10'
}

prof_links['camilo.castillo'] = {
    'ORCID': 'https://orcid.org/0000-0003-3064-1464',
    'Scholar': 'https://scholar.google.com.co/citations?user=m2aL2K8AAAAJ&hl=es',
    'CvLAC': 'https://scienti.minciencias.gov.co/cvlac/EnRecursoHumano/query.do', 
    'Academia': 'https://independent.academia.edu/CAMILOTARAZONA',
    'ResearchGate': 'https://www.researchgate.net/profile/Camilo-Castillo-Tarazona',
    'GitHub': 'https://github.com/CamiloCastillo88'
}

prof_links['leonardo.guarin'] = {
    'ORCID': 'https://orcid.org/0000-0003-3465-9831',
    'CvLAC': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001402283'
}

# 3. Apply to all html files
for f in html_files:
    with open(f, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    modified = False
    profs = soup.find_all('article', class_='prof-card')
    for prof in profs:
        ident = get_identifier(prof)
        if not ident or ident not in prof_links: continue
        
        links_div = prof.find('div', class_='prof-links')
        if not links_div:
            # create one
            links_div = soup.new_tag('div', **{'class': 'prof-links'})
            email_div = prof.find('div', class_='prof-email')
            email_div.insert_after(links_div)
            modified = True
        
        # clear existing and rebuild in order
        links_div.clear()
        for name in ['ORCID', 'Scholar', 'CvLAC', 'Academia', 'ResearchGate', 'GitHub']:
            if name in prof_links[ident]:
                a_tag = soup.new_tag('a', href=prof_links[ident][name], target='_blank')
                if name == 'GitHub':
                    a_tag['rel'] = 'noopener noreferrer'
                a_tag.string = name
                links_div.append(a_tag)
                modified = True
                
    if modified:
        with open(f, 'w') as file:
            file.write(str(soup))
        print(f"Updated {f}")

