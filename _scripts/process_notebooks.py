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
            "html", 
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