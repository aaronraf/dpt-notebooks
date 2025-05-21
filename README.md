# DPT Notebook Collection Website

## Overview

This project creates a dynamic website that automatically displays Marimo notebooks uploaded to a repository. The site will:

1. Render Marimo notebooks as interactive HTML
2. Update automatically when new notebooks are added
3. Provide search and categorization features
4. Maintain a clean, responsive interface

## System Architecture

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│               │     │               │     │               │
│  Repository   │────▶│  Build Script │────▶│  GitHub Pages │
│  (Notebooks)  │     │  (Generator)  │     │  (Website)    │
│               │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
```

<!--
## Implementation Plan

### 1. Set Up the Repository Structure

```
marimo-collection/
├── notebooks/               # Raw .py Marimo notebooks
├── _scripts/                # Processing scripts
│   ├── process_notebooks.py # Converts notebooks to HTML
│   └── generate_site.py     # Builds the website
├── _site/                   # Generated website (gitignored)
├── templates/               # Website templates
│   ├── base.html
│   ├── index.html
│   └── notebook.html
├── static/                  # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── .github/                 # GitHub Actions workflow
│   └── workflows/
│       └── build.yml
└── README.md
```

### 2. Processing Script for Notebooks

Create a Python script to extract metadata and convert notebooks to HTML:

```python
import os
import json
import re
import subprocess
from pathlib import Path
import shutil

def process_notebooks(notebooks_dir, output_dir):
    """Process all Marimo notebooks and extract metadata."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    notebooks = []
    
    for file in Path(notebooks_dir).glob("*.py"):
        # Generate HTML version
        html_output = Path(output_dir) / f"{file.stem}.html"
        
        # Run marimo to convert notebook to HTML
        subprocess.run([
            "marimo", "export", 
            "--format", "html", 
            str(file), 
            "-o", str(html_output)
        ])
        
        # Extract metadata from notebook
        metadata = extract_metadata(file)
        metadata["filename"] = file.name
        metadata["html_path"] = f"notebooks/{file.stem}.html"
        
        notebooks.append(metadata)
    
    # Generate index JSON
    with open(Path(output_dir) / "index.json", "w") as f:
        json.dump(notebooks, f, indent=2)
    
    return notebooks

def extract_metadata(notebook_path):
    """Extract title, description, tags from notebook comments."""
    with open(notebook_path, "r") as f:
        content = f.read()
    
    # Extract title from first line comment or filename
    title_match = re.search(r'#\s*Title:\s*(.*)', content)
    title = title_match.group(1) if title_match else notebook_path.stem.replace("_", " ").title()
    
    # Extract description from comment
    desc_match = re.search(r'#\s*Description:\s*(.*)', content)
    description = desc_match.group(1) if desc_match else ""
    
    # Extract tags from comment
    tags_match = re.search(r'#\s*Tags:\s*(.*)', content)
    tags = []
    if tags_match:
        tags = [tag.strip() for tag in tags_match.group(1).split(",")]
    
    # Extract date from comment or use file modification time
    date_match = re.search(r'#\s*Date:\s*(.*)', content)
    date = date_match.group(1) if date_match else ""
    
    return {
        "title": title,
        "description": description,
        "tags": tags,
        "date": date,
        "last_modified": os.path.getmtime(notebook_path)
    }

if __name__ == "__main__":
    process_notebooks("notebooks", "_site/notebooks")
```

### 3. Website Generator

Create a script to build the static website:

```python
import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def build_site(notebooks_data, templates_dir, static_dir, output_dir):
    """Generate the website from templates and notebook data."""
    # Create directories
    site_dir = Path(output_dir)
    site_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy static files
    static_output = site_dir / "static"
    if static_output.exists():
        shutil.rmtree(static_output)
    shutil.copytree(static_dir, static_output)
    
    # Set up Jinja
    env = Environment(loader=FileSystemLoader(templates_dir))
    
    # Generate index page
    index_template = env.get_template("index.html")
    index_html = index_template.render(
        notebooks=notebooks_data,
        tags=collect_tags(notebooks_data)
    )
    with open(site_dir / "index.html", "w") as f:
        f.write(index_html)
    
    # Generate individual notebook pages
    notebook_template = env.get_template("notebook.html")
    for notebook in notebooks_data:
        notebook_html = notebook_template.render(
            notebook=notebook,
            notebooks=notebooks_data
        )
        notebook_page = site_dir / f"view_{Path(notebook['filename']).stem}.html"
        with open(notebook_page, "w") as f:
            f.write(notebook_html)

def collect_tags(notebooks):
    """Collect all unique tags from notebooks."""
    all_tags = set()
    for notebook in notebooks:
        all_tags.update(notebook.get("tags", []))
    return sorted(list(all_tags))

if __name__ == "__main__":
    # Load processed notebook data
    with open("_site/notebooks/index.json", "r") as f:
        notebooks = json.load(f)
    
    # Build the site
    build_site(notebooks, "templates", "static", "_site")
```

### 4. HTML Templates

Create the base template (`templates/base.html`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Marimo Notebook Collection{% endblock %}</title>
    <link rel="stylesheet" href="static/css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@2.8.2/dist/alpine.min.js" defer></script>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="index.html">Marimo Notebook Collection</a></h1>
            <nav>
                <ul>
                    <li><a href="index.html">Home</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <div class="container">
            <p>Marimo Notebook Collection - Automatically updated when new notebooks are added.</p>
        </div>
    </footer>
    
    <script src="static/js/main.js"></script>
</body>
</html>
```

Create the index template (`templates/index.html`):

```html
{% extends "base.html" %}

{% block title %}Marimo Notebook Collection{% endblock %}

{% block content %}
<div x-data="{ activeTag: 'all' }">
    <div class="search-container">
        <input type="text" id="search" placeholder="Search notebooks..." 
               oninput="filterNotebooks()" class="search-input">
               
        <div class="tag-filters">
            <button x-on:click="activeTag = 'all'" 
                    x-bind:class="{'active': activeTag === 'all'}" 
                    class="tag-button">All</button>
            {% for tag in tags %}
            <button x-on:click="activeTag = '{{ tag }}'"
                    x-bind:class="{'active': activeTag === '{{ tag }}'}"
                    class="tag-button">{{ tag }}</button>
            {% endfor %}
        </div>
    </div>

    <div class="notebooks-grid">
        {% for notebook in notebooks %}
        <div class="notebook-card" 
             x-show="activeTag === 'all' || {{ notebook.tags|tojson }}.includes(activeTag)"
             data-title="{{ notebook.title }}"
             data-description="{{ notebook.description }}"
             data-tags="{{ notebook.tags|join(' ') }}">
            <h2>{{ notebook.title }}</h2>
            <p class="description">{{ notebook.description }}</p>
            <div class="notebook-tags">
                {% for tag in notebook.tags %}
                <span class="tag">{{ tag }}</span>
                {% endfor %}
            </div>
            <div class="notebook-actions">
                <a href="{{ notebook.html_path }}" class="view-button">Interactive View</a>
                <a href="view_{{ notebook.filename|replace('.py', '.html') }}" class="info-button">Details</a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<script>
function filterNotebooks() {
    const searchTerm = document.getElementById('search').value.toLowerCase();
    const cards = document.querySelectorAll('.notebook-card');
    
    cards.forEach(card => {
        const title = card.dataset.title.toLowerCase();
        const description = card.dataset.description.toLowerCase();
        const tags = card.dataset.tags.toLowerCase();
        
        if (title.includes(searchTerm) || 
            description.includes(searchTerm) || 
            tags.includes(searchTerm)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}
</script>
{% endblock %}
```

Create the notebook detail template (`templates/notebook.html`):

```html
{% extends "base.html" %}

{% block title %}{{ notebook.title }} - Marimo Notebook{% endblock %}

{% block content %}
<div class="notebook-detail">
    <h1>{{ notebook.title }}</h1>
    
    <div class="notebook-metadata">
        {% if notebook.date %}
        <div class="metadata-item">
            <span class="metadata-label">Date:</span>
            <span class="metadata-value">{{ notebook.date }}</span>
        </div>
        {% endif %}
        
        <div class="metadata-item">
            <span class="metadata-label">Tags:</span>
            <span class="metadata-value">
                {% for tag in notebook.tags %}
                <span class="tag">{{ tag }}</span>
                {% endfor %}
            </span>
        </div>
    </div>
    
    <div class="notebook-description">
        {{ notebook.description }}
    </div>
    
    <div class="notebook-actions">
        <a href="{{ notebook.html_path }}" class="primary-button">Open Interactive Notebook</a>
        <a href="notebooks/{{ notebook.filename }}" class="secondary-button">Download Source</a>
    </div>
    
    <h2>Related Notebooks</h2>
    <div class="related-notebooks">
        {% set related_count = 0 %}
        {% for nb in notebooks %}
            {% if nb.filename != notebook.filename and (set(nb.tags) & set(notebook.tags)) %}
                {% if related_count < 3 %}
                <div class="related-notebook">
                    <h3>{{ nb.title }}</h3>
                    <p>{{ nb.description[:100] }}{% if nb.description|length > 100 %}...{% endif %}</p>
                    <a href="view_{{ nb.filename|replace('.py', '.html') }}">View Details</a>
                </div>
                {% set related_count = related_count + 1 %}
                {% endif %}
            {% endif %}
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### 5. CSS Styling

Create the styles file (`static/css/styles.css`):

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --bg-color: #f9fafb;
    --card-bg: #ffffff;
    --text-color: #1f2937;
    --text-light: #6b7280;
    --border-color: #e5e7eb;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
}

.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

header {
    background-color: var(--primary-color);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

header h1 {
    font-size: 1.5rem;
    font-weight: 600;
}

header a {
    color: white;
    text-decoration: none;
}

nav ul {
    display: flex;
    list-style: none;
}

nav ul li {
    margin-left: 1.5rem;
}

main {
    padding: 2rem 0;
}

footer {
    background-color: var(--text-color);
    color: white;
    padding: 1rem 0;
    text-align: center;
    margin-top: 2rem;
}

/* Search and filter styles */
.search-container {
    margin-bottom: 2rem;
}

.search-input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 0.375rem;
    font-size: 1rem;
    margin-bottom: 1rem;
}

.tag-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.tag-button {
    background-color: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 0.25rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-size: 0.875rem;
}

.tag-button.active {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

/* Notebook grid */
.notebooks-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.notebook-card {
    background-color: var(--card-bg);
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.notebook-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.notebook-card h2 {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
}

.description {
    color: var(--text-light);
    margin-bottom: 1rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.notebook-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.tag {
    background-color: #e5e7eb;
    color: var(--text-color);
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
}

.notebook-actions {
    display: flex;
    gap: 0.75rem;
}

.view-button, .info-button {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    text-decoration: none;
    font-size: 0.875rem;
    text-align: center;
}

.view-button {
    background-color: var(--primary-color);
    color: white;
    flex: 1;
}

.info-button {
    background-color: var(--bg-color);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    flex: 0.5;
}

/* Notebook detail page */
.notebook-detail {
    background-color: var(--card-bg);
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.notebook-detail h1 {
    font-size: 1.75rem;
    margin-bottom: 1rem;
}

.notebook-metadata {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
    color: var(--text-light);
}

.metadata-label {
    font-weight: 600;
}

.notebook-description {
    margin-bottom: 1.5rem;
    line-height: 1.8;
}

.primary-button, .secondary-button {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 0.375rem;
    text-decoration: none;
    font-weight: 500;
    margin-right: 1rem;
}

.primary-button {
    background-color: var(--primary-color);
    color: white;
}

.secondary-button {
    background-color: white;
    color: var(--text-color);
    border: 1px solid var(--border-color);
}

.notebook-actions {
    margin-bottom: 2rem;
}

.related-notebooks {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.related-notebook {
    background-color: var(--bg-color);
    padding: 1rem;
    border-radius: 0.375rem;
}

.related-notebook h3 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .notebooks-grid {
        grid-template-columns: 1fr;
    }
    
    .notebook-detail {
        padding: 1.5rem;
    }
    
    .related-notebooks {
        grid-template-columns: 1fr;
    }
}
```

### 6. JavaScript Functionality

Create the main JavaScript file (`static/js/main.js`):

```javascript
// Handle filtering notebooks by tag
document.addEventListener('DOMContentLoaded', function() {
    // We're using Alpine.js for most functionality, so this file is minimal
    
    // Handle clicking on tag chips in notebook details
    const tagChips = document.querySelectorAll('.notebook-metadata .tag');
    if (tagChips) {
        tagChips.forEach(tag => {
            tag.addEventListener('click', () => {
                // In a more complex app, this could navigate back to the index
                // with the specific tag selected
                window.location.href = 'index.html?tag=' + encodeURIComponent(tag.textContent);
            });
        });
    }
});
```

### 7. GitHub Actions Workflow

Create a GitHub workflow file (`.github/workflows/build.yml`):

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install marimo jinja2
      
      - name: Process notebooks
        run: |
          mkdir -p _site/notebooks
          python _scripts/process_notebooks.py
      
      - name: Build site
        run: |
          python _scripts/generate_site.py
      
      - name: Deploy to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: _site
          branch: gh-pages
```

### 8. Main Script to Run Locally

Create a script to run the build process locally (`_scripts/build_local.py`):

```python
import os
import subprocess
from pathlib import Path

def build_local():
    """Build the website locally."""
    # Create output directory
    os.makedirs("_site/notebooks", exist_ok=True)
    
    # Process notebooks
    subprocess.run(["python", "_scripts/process_notebooks.py"])
    
    # Generate site
    subprocess.run(["python", "_scripts/generate_site.py"])
    
    print("Website built successfully in _site directory")
    print("To view it locally, run: python -m http.server --directory _site")

if __name__ == "__main__":
    build_local()
``` -->

## How to Use

1. **Setup the Repository**:
   - Create a new GitHub repository
   - Clone it to your computer
   - Set up the folder structure as outlined above
   - Add all the files

2. **Add Notebooks**:
   - Place Marimo notebooks (.py files) in the `notebooks/` directory
   - Add metadata as comments at the top of each notebook:
     ```python
     # Title: Introduction to Data Analysis
     # Description: This notebook introduces basic data analysis concepts
     # Tags: intro, data, analysis
     # Date: 2023-05-15
     ```

3. **Build Locally for Testing**:
   ```bash
   python _scripts/build_local.py
   python -m http.server --directory _site
   ```

4. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit with notebooks"
   git push origin main
   ```

5. **Enable GitHub Pages**:
   - Go to repository settings
   - Under "Pages", select the `gh-pages` branch
   - Your site will be available at `https://[username].github.io/[repository]`

6. **Add New Notebooks**:
   - Simply add new Marimo notebook files to the `notebooks/` directory
   - Push to GitHub
   - The GitHub Actions workflow will automatically rebuild and deploy the site

<!-- ## Next Steps

- Add authentication if needed
- Implement categories for better organization
- Add a search feature with more advanced filtering
- Create a custom domain for the collection -->
