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