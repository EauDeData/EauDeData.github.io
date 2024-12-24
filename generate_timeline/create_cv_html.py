import csv
import json
from datetime import datetime
import random

def parse_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, '%d/%m/%y').strftime('%Y-%m-%d')

def generate_html(events):
    # Generate unique IDs for events
    for idx, event in enumerate(events):
        event['id'] = idx + 1

    with open('styles.css', 'r') as css_file:
        css_content = css_file.read()

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Adrià Molina, CV</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis-timeline/7.7.2/vis-timeline-graph2d.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-timeline/7.7.2/vis-timeline-graph2d.min.js"></script>
    <style>
    {css_content}
    
    #timeline {{
        width: 100%;
        height: 600px;
        margin: 20px 0;
    }}
    
    .vis-item {{
        border-color: #aa0000;
        background-color: #222;
        color: #f7f7f7;
        font-family: 'Holly Bale', sans-serif;
    }}
    
    .vis-item.vis-selected {{
        background-color: #ff0000;
    }}
    
    .timeline-tooltip {{
        position: absolute;
        background: #333;
        border: 2px solid #aa0000;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
        max-width: 300px;
        z-index: 1000;
    }}
    
    .timeline-tooltip img {{
        max-width: 100%;
        height: auto;
    }}
    
    .timeline-tooltip iframe {{
        width: 100%;
        height: 200px;
        border: none;
    }}
    .category-studies {{
    border-color: #4caf50;
    background-color: #a5d6a7;
    color: #1b5e20;
    }}

    .category-job {{
        border-color: #2196f3;
        background-color: #90caf9;
        color: #0d47a1;
    }}

    .category-project {{
        border-color: #ff9800;
        background-color: #ffcc80;
        color: #e65100;
    }}

    .category-divulga {{
        border-color: #9c27b0;
        background-color: #ce93d8;
        color: #4a148c;
    }}

    .category-hack {{
        border-color: #f44336;
        background-color: #ef9a9a;
        color: #b71c1c;
    }}

    .category-conference {{
        border-color: #00bcd4;
        background-color: #80deea;
        color: #006064;
    }}

    .category-paper {{
        border-color: #8bc34a;
        background-color: #dcedc8;
        color: #33691e;
    }}

    .category-award {{
        border-color: #ffeb3b;
        background-color: #fff9c4;
        color: #f57f17;
    }}

    </style>

</head>
<body>

    <div id="header">
        <h2>Adrià Molina, CV</h2>
    </div>
    <nav>
        <a href="../index.html">Torna a la pàgina principal.</a>
    </nav>
    <div id="timeline"></div>
    <script>
        const events = {json.dumps(events)};
        
        const items = new vis.DataSet(events.map(event => ({{
            id: event.id,
            content: event.name,
            start: event.start_date,
            end: event.end_date,
            type: event.end_date ? 'range' : 'point',
            className: `category-${event.get("category")}`, // Dynamic class based on category
            href: event.href
        }})));

        
        const options = {{
            height: '500px',
            orientation: 'top',
            stack: true,
            zoomMin: 1000 * 60 * 60 * 24 * 30,
            zoomMax: 1000 * 60 * 60 * 24 * 365 * 5
        }};
        
        const container = document.getElementById('timeline');
        const timeline = new vis.Timeline(container, items, options);
        
        let tooltip = null;
        
        timeline.on('itemover', (properties) => {{
            const item = items.get(properties.item);
            if (item.href) {{
                if (!tooltip) {{
                    tooltip = document.createElement('div');
                    tooltip.className = 'timeline-tooltip';
                    document.body.appendChild(tooltip);
                }}
                
                const isImage = /\\.(jpg|jpeg|png|gif)$/i.test(item.href);
                tooltip.innerHTML = isImage 
                    ? `<img src="${{item.href}}" alt="${{item.content}}">`
                    : `<iframe src="${{item.href}}"></iframe>`;
                
                const rect = properties.event.target.getBoundingClientRect();
                tooltip.style.left = `${{rect.left}}px`;
                tooltip.style.top = `${{rect.bottom + 10}}px`;
            }}
        }});
        
        timeline.on('itemout', () => {{
            if (tooltip) {{
                tooltip.remove();
                tooltip = null;
            }}
        }});
        
        timeline.on('click', (properties) => {{
            if (properties.item) {{
                const item = items.get(properties.item);
                if (item.href) {{
                    window.open(item.href, '_blank');
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    return html_content

def main():
    events = []
    with open('curriculum.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            events.append({
                'name': row['name'],
                'start_date': parse_date(row['start_date']),
                'end_date': parse_date(row['end_date']),
                'category': row['category'],
                'href': row['href']
            })
            
    random.shuffle(events)
    html_content = generate_html(events)
    
    with open('timeline.html', 'w') as file:
        file.write(html_content)

if __name__ == '__main__':
    main()