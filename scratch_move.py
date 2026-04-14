import re

# 1. Grab Margui from modelado-matematico
mm_content = open("modelado-matematico.html").read()
# Find article block for Margui
margui_match = re.search(r'(<article class="prof-card">.*?Margui Romero.*?</article>)', mm_content, flags=re.DOTALL)
if margui_match:
    margui_html = margui_match.group(1)
    # Inject into gestion-del-conocimiento
    gc_content = open("gestion-del-conocimiento.html").read()
    if "Margui Romero" not in gc_content:
        # Find the end of prof-grid
        # It's usually before </section> of prof-grid
        # Let's just insert before the last </article> \n </div> \n </div> \n </section>
        # Actually easier to find the last </article> in the grid.
        last_article_pos = gc_content.rfind('</article>')
        if last_article_pos != -1:
            insertion_point = last_article_pos + len('</article>')
            new_gc = gc_content[:insertion_point] + "\n\n" + f"                <!-- O MARGUI -->\n                {margui_html}" + gc_content[insertion_point:]
            open("gestion-del-conocimiento.html", "w").write(new_gc)
            print("Margui added to gestion-del-conocimiento.")

# 2. Grab Emma from gestion-del-conocimiento
# We should read it afresh in case Emma was there.
gc_content = open("gestion-del-conocimiento.html").read()
emma_match = re.search(r'(<article class="prof-card">.*?Emma Julieth Camargo Diaz.*?</article>)', gc_content, flags=re.DOTALL)
if emma_match:
    emma_html = emma_match.group(1)
    # Inject into sistemas-agroalimentarios
    sa_content = open("sistemas-agroalimentarios.html").read()
    if "Emma Julieth Camargo" not in sa_content:
        last_article_pos = sa_content.rfind('</article>')
        if last_article_pos != -1:
            insertion_point = last_article_pos + len('</article>')
            new_sa = sa_content[:insertion_point] + "\n\n" + f"                <!-- EMMA -->\n                {emma_html}" + sa_content[insertion_point:]
            open("sistemas-agroalimentarios.html", "w").write(new_sa)
            print("Emma added to sistemas-agroalimentarios.")

print("Done")
