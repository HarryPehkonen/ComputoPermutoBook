#!/usr/bin/env python3
"""
Master Build Script for ComputoPermutoBook

Generates all chapters from TOML sources, validates all examples,
and creates unified downloads. Designed to be GitHub Actions compatible.

Usage:
    python scripts/build_all_chapters.py
    python scripts/build_all_chapters.py --validate
    python scripts/build_all_chapters.py --html
"""

import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import our chapter generator
from generate_book_chapter import BookChapterGenerator

try:
    import tomli
except ImportError:
    print("Error: tomli package not found. Please install with: pip install tomli")
    sys.exit(1)


class BookBuilder:
    def __init__(self, source_dir: Path = None, output_dir: Path = None, computo_path: str = "computo"):
        self.source_dir = source_dir or Path("book-source")
        self.output_dir = output_dir or Path("new_way")
        self.computo_path = computo_path
        self.chapter_files = []
        self.chapter_data = {}
        self.validation_results = {}
        
    def discover_chapters(self):
        """Find all chapter TOML files."""
        pattern = "ch*.toml"
        self.chapter_files = sorted(list(self.source_dir.glob(pattern)))
        
        if not self.chapter_files:
            print(f"No chapter files found in {self.source_dir}")
            return False
            
        print(f"Found {len(self.chapter_files)} chapter files:")
        for chapter_file in self.chapter_files:
            print(f"  {chapter_file.name}")
        return True

    def generate_single_chapter(self, chapter_file: Path, validate: bool = False):
        """Generate a single chapter."""
        try:
            generator = BookChapterGenerator(chapter_file, self.output_dir, self.computo_path)
            
            success = True
            if validate:
                print(f"  Validating examples...")
                success = generator.validate_all_examples()
                generator.generate_test_report()
            
            print(f"  Generating markdown...")
            generator.generate_markdown()
            
            print(f"  Saving examples...")
            generator.save_examples()
            
            chapter_num = generator.chapter_data['chapter']['number']
            return {
                'chapter': chapter_num,
                'file': chapter_file,
                'success': success,
                'validation_results': generator.example_results if validate else None
            }
            
        except Exception as e:
            return {
                'chapter': chapter_file.stem,
                'file': chapter_file,
                'success': False,
                'error': str(e)
            }

    def generate_all_chapters(self, validate: bool = False):
        """Generate all chapters."""
        print(f"Generating {len(self.chapter_files)} chapters...")
        
        results = []
        for chapter_file in self.chapter_files:
            print(f"\nProcessing {chapter_file.name}:")
            result = self.generate_single_chapter(chapter_file, validate)
            results.append(result)
        
        return results

    def create_unified_downloads(self):
        """Create unified download packages."""
        print("\nCreating unified downloads...")
        
        code_dir = self.output_dir / "code"
        if not code_dir.exists():
            print("No code directory found - skipping unified downloads")
            return
        
        # Create unified zip with all examples
        unified_zip = self.output_dir / "download_all_examples.zip"
        with zipfile.ZipFile(unified_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in code_dir.rglob('*'):
                if file_path.is_file():
                    arc_name = file_path.relative_to(code_dir.parent)
                    zf.write(file_path, arc_name)
        
        print(f"Created unified download: {unified_zip}")

    def create_build_summary(self, results):
        """Create a build summary report."""
        summary_file = self.output_dir / "build_summary.md"
        
        total_chapters = len(results)
        successful_chapters = sum(1 for r in results if r['success'])
        failed_chapters = total_chapters - successful_chapters
        
        total_examples = 0
        passed_examples = 0
        failed_examples = 0
        
        for result in results:
            if result.get('validation_results'):
                for validation in result['validation_results']:
                    total_examples += 1
                    if validation['result']['success']:
                        passed_examples += 1
                    else:
                        failed_examples += 1
        
        content = f"""# Build Summary

**Generated**: {Path().cwd()}

## Chapter Generation

- **Total Chapters**: {total_chapters}
- **Successful**: {successful_chapters}
- **Failed**: {failed_chapters}

"""
        
        if total_examples > 0:
            content += f"""## Example Validation

- **Total Examples**: {total_examples}
- **Passed**: {passed_examples}
- **Failed**: {failed_examples}

"""
        
        content += "## Chapter Details\n\n"
        
        for result in sorted(results, key=lambda x: str(x['chapter'])):
            status = "PASS" if result['success'] else "FAIL"
            content += f"- **{status}** Chapter {result['chapter']}"
            
            if 'error' in result:
                content += f" - Error: {result['error']}"
            elif result.get('validation_results'):
                chapter_examples = len(result['validation_results'])
                chapter_passed = sum(1 for v in result['validation_results'] if v['result']['success'])
                content += f" - Examples: {chapter_passed}/{chapter_examples}"
            
            content += "\n"
        
        with open(summary_file, 'w') as f:
            f.write(content)
        
        print(f"Build summary: {summary_file}")
        return successful_chapters == total_chapters


def main():
    parser = argparse.ArgumentParser(description="Build all book chapters")
    parser.add_argument("--source-dir", default="book-source", help="Source directory with TOML files")
    parser.add_argument("--output-dir", default="new_way", help="Output directory")
    parser.add_argument("--computo-path", default="computo", help="Path to computo executable")
    parser.add_argument("--validate", action="store_true", help="Validate all examples")
    parser.add_argument("--html", action="store_true", help="Generate HTML output (future)")
    
    args = parser.parse_args()
    
    builder = BookBuilder(
        source_dir=Path(args.source_dir),
        output_dir=Path(args.output_dir),
        computo_path=args.computo_path
    )
    
    # Discover chapters
    if not builder.discover_chapters():
        return 1
    
    # Generate all chapters
    results = builder.generate_all_chapters(validate=args.validate)
    
    # Create unified downloads
    builder.create_unified_downloads()
    
    # HTML generation
    if args.html:
        print("\nGenerating HTML files...")
        import subprocess
        result = subprocess.run([
            sys.executable, "scripts/generate_html.py",
            "--input-dir", str(args.output_dir),
            "--output-dir", "docs"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("HTML generation completed successfully!")
        else:
            print(f"HTML generation failed: {result.stderr}")
            success = False
    
    # Create build summary
    success = builder.create_build_summary(results)
    
    if success:
        print("\nBuild completed successfully!")
        return 0
    else:
        print("\nBuild completed with errors!")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 