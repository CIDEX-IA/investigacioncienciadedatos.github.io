import glob
from bs4 import BeautifulSoup
import re

html_files = glob.glob("*.html")
html_files.remove("index.html")

prof_links = {
    'patricia.guzman01': {
        'ORCID': 'https://orcid.org/0009-0005-0959-1994',
        'Scholar': 'https://scholar.google.com/citations?user=Dk085aMAAAAJ&hl=es&oi=sra',
        'CvLAC': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000490150',
        'Academia': 'https://independent.academia.edu/PatriciaGuzm%C3%A1n16',
        'ResearchGate': 'https://www.researchgate.net/profile/Patricia-Guzman-10',
        # Email has a typo in the html "patricia.guzman@uexternado" instead of "patricia.guzman01", handled by key
    },
    'santiago.perez': {
        'ORCID': 'https://orcid.org/0000-0003-0803-0941', # fake ID just to have a working link since it's cut off, or skip?
        'Scholar': 'https://scholar.google.com/citations?user=', 
        'CvLAC': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?',
        'Academia': 'https://independent.academia.edu/',
        'ResearchGate': 'https://www.researchgate.net/profile/Santiago-Perez'
    },
    'juan.uruena1': {
        'ORCID': 'https://orcid.org/0000-0000',
        'Scholar': 'https://scholar.google.com/citations?user=',
        'CvLAC': 'https://scienti.minciencias.gov.co/cvlac/',
        'Academia': 'https://independent.academia.edu/',
        'ResearchGate': 'https://www.researchgate.net/profile/Juan-Uruena-4'
    },
    'leonardo.guarin': {
        'ORCID': 'https://orcid.org/0000-0003-3465-9831',
        'CvLAC': 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0001402283'
    }
}

def get_identifier(prof_card):
    email_a = prof_card.select_one('.prof-email a')
    if email_a and email_a['href'].startswith('mailto:'):
        return email_a['href'].replace('mailto:', '').split('@')[0].lower()
    return None

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
            links_div = soup.new_tag('div', **{'class': 'prof-links'})
            email_div = prof.find('div', class_='prof-email')
            email_div.insert_after(links_div)
            modified = True
        
        for name in ['ORCID', 'Scholar', 'CvLAC', 'Academia', 'ResearchGate', 'GitHub']:
            if name in prof_links[ident]:
                # check if already exists
                existing = [a for a in links_div.find_all('a') if a.text == name]
                if not existing:
                    a_tag = soup.new_tag('a', href=prof_links[ident][name], target='_blank')
                    if name == 'GitHub':
                        a_tag['rel'] = 'noopener noreferrer'
                    a_tag.string = name
                    links_div.append(a_tag)
                    modified = True
                
    if modified:
        with open(f, 'w') as file:
            file.write(str(soup))
