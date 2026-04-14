import re

html_file = "modelado-matematico.html"
content = open(html_file).read()

# Split into articles
articles = re.split(r'(<article class="prof-card">.*?</article>)', content, flags=re.DOTALL)

for i, art in enumerate(articles):
    if not art.startswith('<article'):
        continue
        
    # Find all prof-links blocks
    link_blocks = re.findall(r'(<div class="prof-links">.*?</div>)', art, flags=re.DOTALL)
    
    if len(link_blocks) > 1:
        # Sort link blocks by length descending to keep the most comprehensive one
        link_blocks_sorted = sorted(link_blocks, key=len, reverse=True)
        best_block = link_blocks_sorted[0]
        
        # We want to remove all link blocks
        clean_art = art
        for lb in link_blocks:
            clean_art = clean_art.replace(lb, "", 1)
            
        # Insert the best block right after the prof-email block
        clean_art = re.sub(
            r'(<div class="prof-email">.*?</div>)',
            r'\1\n                        ' + best_block,
            clean_art,
            flags=re.DOTALL
        )
        
        # Clean up empty lines that might have been left behind
        clean_art = re.sub(r'\n\s*\n\s*\n', '\n\n', clean_art)
        
        articles[i] = clean_art

new_content = "".join(articles)

if new_content != content:
    open(html_file, "w").write(new_content)
    print("Fixed duplicates in modelado-matematico.html")
else:
    print("No duplicates found to fix.")
