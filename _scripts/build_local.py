import os
import subprocess
from pathlib import Path

def build_local():
    """Build the website locally."""
    # Create output directory
    os.makedirs("_site/notebooks", exist_ok=True)
    
    # Process notebooks
    subprocess.run(["python3", "_scripts/process_notebooks.py"])
    
    # Generate site
    subprocess.run(["python3", "_scripts/generate_site.py"])
    
    print("Website built successfully in _site directory")
    print("To view it locally, run: python3 -m http.server --directory _site")

if __name__ == "__main__":
    build_local()