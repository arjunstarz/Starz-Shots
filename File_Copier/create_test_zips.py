#!/usr/bin/env python3
"""
Script to create sample zip files for testing the reference builder functionality.
"""

import zipfile
from pathlib import Path

def create_test_zips():
    """Create sample zip files for testing."""
    
    # Create test_zips directory
    zip_dir = Path("test_zips")
    zip_dir.mkdir(exist_ok=True)
    
    # Create first zip file
    with zipfile.ZipFile(zip_dir / "sample1.zip", 'w') as zip1:
        zip1.writestr("document1.txt", "This is document 1 content.")
        zip1.writestr("image1.jpg", "Fake image 1 content.")
        zip1.writestr("data1.csv", "Name,Value\nTest1,100\nTest2,200")
        
    print("Created sample1.zip with: document1.txt, image1.jpg, data1.csv")
    
    # Create second zip file
    with zipfile.ZipFile(zip_dir / "sample2.zip", 'w') as zip2:
        zip2.writestr("report.docx", "This is a report document.")
        zip2.writestr("presentation.pptx", "This is a presentation.")
        zip2.writestr("config.json", '{"setting": "value"}')
        zip2.writestr("subfolder/nested_file.txt", "This is a nested file.")
        
    print("Created sample2.zip with: report.docx, presentation.pptx, config.json, nested_file.txt")
    
    # Create third zip file
    with zipfile.ZipFile(zip_dir / "sample3.zip", 'w') as zip3:
        zip3.writestr("script.py", "print('Hello World')")
        zip3.writestr("readme.md", "# Sample Project")
        zip3.writestr("requirements.txt", "requests==2.25.1")
        
    print("Created sample3.zip with: script.py, readme.md, requirements.txt")
    
    print(f"\nAll test zip files created in: {zip_dir.absolute()}")
    print("\nExpected reference file content:")
    print("document1.txt")
    print("image1.jpg") 
    print("data1.csv")
    print("report.docx")
    print("presentation.pptx")
    print("config.json")
    print("nested_file.txt")
    print("script.py")
    print("readme.md")
    print("requirements.txt")

if __name__ == "__main__":
    create_test_zips()
