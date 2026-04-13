import re

with open('evento.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_css = """
        :root {
            /* Futuristic Dark/Cyan Palette based on the image */
            --bg-deep: #021217;
            --bg-card: #062329;
            --cyan-main: #18d2cc;
            --cyan-dark: #0b5e61;
            --cyan-soft: rgba(24, 210, 204, 0.12);
            --text-main: #e2f1f4;
            --text-muted: #8eb9bc;
            --white: #ffffff;
            --border: #13464b;
            --shadow: 0 14px 40px rgba(0, 0, 0, 0.4);
            --radius-lg: 20px;
            --radius-md: 14px;
            --radius-sm: 8px;
            --max-width: 1000px;
        }

        * {
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        body {
            margin: 0;
            color: var(--text-main);
            background: var(--bg-deep); /* Dark background */
            line-height: 1.65;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        img {
            max-width: 100%;
            display: block;
        }

        .container {
            width: min(var(--max-width), calc(100% - 2rem));
            margin: 0 auto;
        }

        .section {
            padding: 5rem 0;
        }

        .eyebrow {
            display: inline-block;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--cyan-main);
            margin-bottom: 0.8rem;
        }

        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.92);
            margin-bottom: 2rem;
            transition: opacity 0.2s ease;
        }

        .back-link:hover {
            opacity: 0.8;
            color: var(--cyan-main);
        }

        .hero-evento {
            padding: 5rem 0 7rem;
            background: linear-gradient(135deg, #021a22 0%, #063e46 100%);
            color: var(--white);
            position: relative;
            overflow: hidden;
        }
        
        .hero-evento::after {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: radial-gradient(circle at 80% 20%, rgba(24,210,204,0.15) 0%, transparent 50%);
            pointer-events: none;
        }

        .hero-evento h1 {
            font-size: clamp(2.2rem, 3.5vw, 3.8rem);
            line-height: 1.1;
            margin: 0 0 1.5rem;
            max-width: 900px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }

        .event-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            margin-top: 2rem;
            font-size: 1.05rem;
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            background: rgba(0, 0, 0, 0.3);
            padding: 0.75rem 1.25rem;
            border-radius: var(--radius-sm);
            border: 1px solid rgba(24, 210, 204, 0.2);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            backdrop-filter: blur(5px);
        }

        .meta-icon {
            font-size: 1.2rem;
        }

        .content-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow);
            padding: 3rem;
            margin-top: -5rem;
            position: relative;
            z-index: 10;
        }

        .agenda-section {
            margin-bottom: 3.5rem;
        }

        .agenda-section:last-child {
            margin-bottom: 0;
        }

        .agenda-section h2 {
            font-size: 1.7rem;
            color: var(--cyan-main);
            margin-top: 0;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border);
            text-shadow: 0 0 10px rgba(24,210,204,0.3);
        }

        .agenda-item {
            display: grid;
            grid-template-columns: 140px 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
            align-items: start;
        }

        @media (max-width: 600px) {
            .agenda-item {
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }
        }

        .item-time {
            font-weight: 700;
            color: var(--cyan-main);
            background: var(--cyan-soft);
            padding: 0.5rem 0.8rem;
            border-radius: var(--radius-sm);
            font-size: 0.95rem;
            text-align: center;
            display: inline-block;
            border: 1px solid rgba(24, 210, 204, 0.2);
        }

        .item-content h3 {
            margin: 0 0 0.5rem;
            font-size: 1.25rem;
            color: var(--white);
        }

        .item-content p {
            margin: 0 0 0.5rem;
            color: var(--text-muted);
        }
        
        .item-content strong {
            color: var(--text-main);
        }

        .speaker-info {
            background: rgba(0,0,0,0.2);
            border-left: 4px solid var(--cyan-main);
            padding: 1rem;
            border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
            margin-top: 1rem;
        }

        .speaker-info strong {
            display: block;
            color: var(--cyan-main);
            margin-bottom: 0.25rem;
        }

        .tag-list {
            list-style: none;
            padding: 0;
            margin: 0.5rem 0 0;
        }

        .tag-list li {
            position: relative;
            padding-left: 1.5rem;
            margin-bottom: 0.4rem;
            color: var(--text-muted);
        }

        .tag-list li::before {
            content: "•";
            color: var(--cyan-main);
            font-weight: bold;
            font-size: 1.2rem;
            position: absolute;
            left: 0;
            top: -2px;
        }
"""

new_html = re.sub(r'<style>.*?</style>', f'<style>\n{new_css}\n    </style>', html, flags=re.DOTALL)

with open('evento.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
