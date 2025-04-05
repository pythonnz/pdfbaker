"""Main entry point for the document generator."""

import importlib
import os
import sys
from pathlib import Path

import yaml

from .render import create_env


def _deep_merge(base, update):
    """Recursively merge two dictionaries.

    Values in update will override those in base, except for dictionaries
    which will be merged recursively.
    """
    merged = base.copy()

    for key, value in update.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value

    return merged


def main(config_path=None):
    """Main function for the document generator."""
    # Get config path from arguments if not provided
    if config_path is None:
        if len(sys.argv) < 2:
            print("Error: Config file path is required")
            print("Usage: python -m pdfbaker <config_file_path>")
            return 1
        config_path = sys.argv[1]
    
    # Load main configuration
    config_path = Path(config_path).resolve()  # Get absolute path
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1
        
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    # Create root output directories relative to config file
    base_dir = config_path.parent
    build_dir = base_dir / "build"
    dist_dir = base_dir / "dist"
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(dist_dir, exist_ok=True)

    # Allow document_paths to be absolute or relative to config file
    documents = config.get("documents", [])
    document_paths = {}
    
    for doc_name in documents:
        # Check if document path is specified
        if isinstance(doc_name, dict):
            # Format: {"name": "doc_name", "path": "/absolute/path/to/doc"}
            doc_path = Path(doc_name["path"])
            doc_name = doc_name["name"]
        else:
            # Default: document in subdirectory with same name as doc_name
            doc_path = base_dir / doc_name
        
        # Store the absolute path
        document_paths[doc_name] = doc_path.resolve()

    # Process each document
    for doc_name, doc_path in document_paths.items():
        if not doc_path.is_dir():
            print(f'Warning: Directory missing for document "{doc_name}" at {doc_path} - skipping')
            continue
        
        bake_path = doc_path / "bake.py"
        if not bake_path.exists():
            print(f'Warning: bake.py missing for document "{doc_name}" - skipping')
            continue
            
        config_yml_path = doc_path / "config.yml"
        if not config_yml_path.exists():
            print(f'Warning: config.yml missing for document "{doc_name}" - skipping')
            continue
        
        print(f'Processing document "{doc_name}" from {doc_path}...')
        
        # Load document-specific bake
        doc_bake = importlib.util.spec_from_file_location(
            f"documents.{doc_name}.bake",
            bake_path
        )
        module = importlib.util.module_from_spec(doc_bake)
        doc_bake.loader.exec_module(module)
        
        # Merge document configuration
        with open(config_yml_path, encoding="utf-8") as f:
            doc_config = yaml.safe_load(f)
        merged_config = _deep_merge(config, doc_config)

        # Create document-specific output directories
        doc_build_dir = build_dir / doc_name
        doc_dist_dir = dist_dir / doc_name
        os.makedirs(doc_build_dir, exist_ok=True)
        os.makedirs(doc_dist_dir, exist_ok=True)
        
        # Clean document-specific output directories
        for dir_path in [doc_build_dir, doc_dist_dir]:
            for file in os.listdir(dir_path):
                file_path = dir_path / file
                if os.path.isfile(file_path):
                    os.remove(file_path)

        # Prepare paths for the document processor
        paths = {
            "doc_dir": doc_path,
            "templates_dir": doc_path / "templates",
            "pages_dir": doc_path / "pages",
            "images_dir": doc_path / "images",
            "build_dir": doc_build_dir,
            "dist_dir": doc_dist_dir,
        }

        # Prepare Jinja environment
        jinja_env = create_env(paths["templates_dir"])

        # Process the document
        module.process_document(paths, merged_config, jinja_env)
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
