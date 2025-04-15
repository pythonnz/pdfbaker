import shutil
from pathlib import Path
from pdfbaker.baker import PDFBaker


def test_examples() -> None:
    """Test all examples."""
    examples_dir = Path(__file__).parent.parent / "examples"
    test_dir = Path(__file__).parent
    
    # Create build and dist directories
    build_dir = test_dir / "build"
    dist_dir = test_dir / "dist"
    build_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)
    
    # Copy and modify examples config
    config = examples_dir / "examples.yaml"
    test_config = test_dir / "examples.yaml"
    shutil.copy(config, test_config)
    
    # Modify paths in config
    with open(test_config) as f:
        content = f.read()
    content = content.replace("build_dir: build", f"build_dir: {build_dir}")
    content = content.replace("dist_dir: dist", f"dist_dir: {dist_dir}")
    with open(test_config, "w") as f:
        f.write(content)
    
    # Run baker
    baker = PDFBaker(test_config, quiet=True, keep_build=True)
    baker.bake() 
