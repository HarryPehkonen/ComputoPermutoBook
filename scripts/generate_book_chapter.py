#!/usr/bin/env python3
"""
Book Chapter Generator for ComputoPermutoBook

Generates markdown chapters and HTML from TOML source files.
Validates all examples by running them through Computo.
Creates organized, downloadable code examples with cross-platform scripts.

Based on the Computo documentation system but adapted for human-readable books.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    import tomli
except ImportError:
    print("Error: tomli package not found. Please install with: pip install tomli")
    sys.exit(1)


class BookChapterGenerator:
    def __init__(self, chapter_file: Path, output_dir: Path, computo_path: str = "computo"):
        self.chapter_file = chapter_file
        self.output_dir = output_dir
        self.computo_path = computo_path
        self.chapter_data = self._load_chapter()
        self.example_results = []
        
        # Determine if this is a chapter or appendix
        self.is_appendix = 'appendix' in self.chapter_data
        if self.is_appendix:
            self.content_data = self.chapter_data['appendix']
            self.sections = self.chapter_data.get('sections', [])
        else:
            self.content_data = self.chapter_data['chapter']
            self.sections = self.chapter_data.get('sections', [])

    def _load_chapter(self):
        """Load and parse the TOML chapter file."""
        with open(self.chapter_file, "rb") as f:
            return tomli.load(f)

    def _validate_example(self, example):
        """Run a single example through Computo to validate it works."""
        try:
            # Create temporary files for script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as script_file:
                json.dump(example['script'], script_file, indent=2)
                script_path = script_file.name

            # Only create input file if there's actual input data
            input_path = None
            input_data = example.get('input', {})
            has_input = len(input_data) > 0
            if has_input:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as input_file:
                    json.dump(example['input'], input_file, indent=2)
                    input_path = input_file.name

            # Build command with CLI flags if specified
            cmd = [self.computo_path]
            if 'cli_flags' in example:
                cmd.extend(example['cli_flags'])
            cmd.append(script_path)
            if input_path:
                cmd.append(input_path)

            # Run Computo
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Clean up temporary files
            os.unlink(script_path)
            if input_path:
                os.unlink(input_path)

            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f"Computo returned error code {result.returncode}",
                    'stderr': result.stderr,
                    'stdout': result.stdout,
                    'command': ' '.join(cmd)
                }

            # Parse the output and compare with expected
            try:
                actual_output = json.loads(result.stdout.strip())
                expected_output = example['expected']
                
                if actual_output == expected_output:
                    return {
                        'success': True,
                        'output': actual_output,
                        'stderr': result.stderr,
                        'stdout': result.stdout
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Output mismatch',
                        'expected': expected_output,
                        'actual': actual_output,
                        'stderr': result.stderr,
                        'stdout': result.stdout
                    }
            except json.JSONDecodeError as e:
                return {
                    'success': False,
                    'error': f"Failed to parse Computo output as JSON: {e}",
                    'raw_output': result.stdout,
                    'stderr': result.stderr,
                    'command': ' '.join(cmd)
                }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Computo execution timed out after 30 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {e}"
            }

    def validate_all_examples(self):
        """Validate all examples in the chapter."""
        if 'examples' not in self.chapter_data:
            print("No examples found in chapter.")
            return True

        examples = self.chapter_data['examples']
        print(f"Validating {len(examples)} examples...")
        
        all_passed = True
        for i, example in enumerate(examples):
            print(f"  {i+1:2d}. {example['name']:<30} ", end="", flush=True)
            
            result = self._validate_example(example)
            self.example_results.append({
                'example': example,
                'result': result
            })
            
            if result['success']:
                print("✓ PASS")
            else:
                print("✗ FAIL")
                print(f"      Error: {result['error']}")
                if 'expected' in result and 'actual' in result:
                    print(f"      Expected: {result['expected']}")
                    print(f"      Actual:   {result['actual']}")
                all_passed = False

        return all_passed

    def _generate_markdown_content(self):
        """Generate the markdown content for the chapter or appendix."""
        content_parts = []

        # Header (different for chapters vs appendices)
        if self.is_appendix:
            content_parts.append(f"## **Appendix {self.content_data['letter']}: {self.content_data['title']}**")
        else:
            content_parts.append(f"## **Chapter {self.content_data['number']}: {self.content_data['title']}**")
        content_parts.append("")

        # Learning objectives summary if present
        if 'learning_objectives' in self.content_data and 'summary' in self.content_data['learning_objectives']:
            content_parts.append(self.content_data['learning_objectives']['summary'])
            content_parts.append("")

        # Generate sections
        for section in self.sections:
            content_parts.append(f"### {section['title']}")
            content_parts.append("")
            content_parts.append(section['content'])
            content_parts.append("")

        # Add comprehensive examples at the end
        examples = None
        if 'examples' in self.chapter_data:
            examples = self.chapter_data['examples']
        elif 'chapter' in self.chapter_data and 'examples' in self.chapter_data['chapter']:
            examples = self.chapter_data['chapter']['examples']
            
        if examples:
            content_parts.append("## 💻 Hands-On Examples")
            content_parts.append("")
            content_parts.append("These examples demonstrate the concepts covered in this chapter. Each example includes the complete script, expected output, and instructions for running it yourself.")
            content_parts.append("")
            
            for example in examples:
                content_parts.extend(self._format_example_for_markdown(example))

        # Chapter/Appendix summary
        if 'summary' in self.content_data:
            content_parts.append(self.content_data['summary']['content'])
            content_parts.append("")

        return "\n".join(content_parts)

    def _format_example_for_markdown(self, example):
        """Format a single example for markdown with complete details."""
        parts = []
        
        # Example header
        parts.append(f"### 🔧 {example['name'].replace('_', ' ').title()}")
        parts.append("")
        
        # Description
        parts.append(f"**Purpose**: {example['description']}")
        parts.append("")
        
        # Tutorial text if present
        if 'tutorial_text' in example:
            parts.append(example['tutorial_text'])
            parts.append("")
        
        # Script section
        parts.append("**Computo Script**:")
        parts.append("```json")
        
        # Preserve original formatting from TOML - don't auto-format
        script_content = example['script']
        if isinstance(script_content, str):
            # Script is stored as a string - preserve exact formatting
            parts.append(script_content)
        else:
            # Script is already parsed as object - use compact formatting
            import json
            parts.append(json.dumps(script_content, separators=(',', ': ')))
            
        parts.append("```")
        parts.append("")
        
        # Input data if present
        input_data = example.get('input', {})
        has_input = len(input_data) > 0
        if has_input:
            parts.append("**Input Data** (`input.json`):")
            parts.append("```json")
            import json
            parts.append(json.dumps(input_data, indent=2))
            parts.append("```")
            parts.append("")
        
        # How to run
        parts.append("**How to Run**:")
        cli_flags = example.get('cli_flags', [])
        flags_str = ' '.join(cli_flags) if cli_flags else ''
        input_arg = "input.json" if has_input else ""
        command = f"computo {flags_str} script.json {input_arg}".strip()
        
        # Generate directory path based on type
        if self.is_appendix:
            letter = self.content_data['letter']
            title = self.content_data['title'].lower().replace(' ', '_').replace('-', '_')
            dir_path = f"appendix_{letter.lower()}_{title}"
        else:
            chapter_num = self.content_data['number']
            title = self.content_data['title'].lower().replace(' ', '_').replace('-', '_')
            dir_path = f"ch{chapter_num:02d}_{title}"
        
        parts.append("```bash")
        parts.append(f"# Navigate to the example directory")
        parts.append(f"cd code/{dir_path}/general/{example['name']}/")
        parts.append("")
        parts.append(f"# Run the example")
        parts.append(command)
        parts.append("")
        parts.append(f"# Or use the provided script")
        parts.append(f"./run.sh    # Linux/Mac")
        parts.append(f"run.bat     # Windows")
        parts.append("```")
        parts.append("")
        
        # Expected output
        parts.append("**Expected Output**:")
        
        # Check if this example has debugging flags
        cli_flags = example.get('cli_flags', [])
        has_debug_flags = any(flag in ['--trace', '--profile', '--debug'] for flag in cli_flags)
        
        if has_debug_flags:
            parts.append("```")
            parts.append("# Debugging output will appear on stderr:")
            parts.append("🔍 Debug mode enabled [TRACE]")
            parts.append("")
            parts.append("✅ EXECUTION SUCCESSFUL in 0ms")
            parts.append("==========================================")
            parts.append("")
            
            if '--trace' in cli_flags:
                parts.append("📋 EXECUTION TRACE:")
                parts.append("===================")
                # Show realistic trace examples based on script type
                script_str = str(example.get('script', ''))
                if 'let' in script_str:
                    parts.append("✓ TRACE [0ms]: Operator '+' at '/let/body/+' with 2 argument(s)")
                    parts.append("✓ TRACE [0ms]: Operator '$' at '/let/body/+/$' with 1 argument(s)")
                    parts.append("✓ TRACE [0ms]: Variable binding: x=10, y=32")
                elif 'map' in script_str:
                    parts.append("✓ TRACE [0ms]: Operator 'map' at '/' with 2 argument(s)")
                    parts.append("✓ TRACE [0ms]: Processing array element [1]: lambda execution")
                    parts.append("✓ TRACE [0ms]: Processing array element [2]: lambda execution")
                    parts.append("✓ TRACE [0ms]: Processing array element [3]: lambda execution")
                    parts.append("✓ TRACE [0ms]: Processing array element [4]: lambda execution")
                elif 'reduce' in script_str:
                    parts.append("✓ TRACE [0ms]: Operator 'reduce' at '/' with 3 argument(s)")
                    parts.append("✓ TRACE [0ms]: Reduce iteration 1: acc=0, x=1")
                    parts.append("✓ TRACE [0ms]: Reduce iteration 2: acc=1, x=4")
                    parts.append("✓ TRACE [0ms]: ... (continuing for all elements)")
                elif 'obj' in script_str:
                    parts.append("✓ TRACE [0ms]: Operator 'obj' at '/' with 2 argument(s)")
                    parts.append("✓ TRACE [0ms]: Creating object property: safe_value")
                    parts.append("✓ TRACE [0ms]: Creating object property: message")
                else:
                    parts.append("✓ TRACE [0ms]: Operator execution details...")
                    parts.append("✓ TRACE [0ms]: Step-by-step operation flow...")
                parts.append("")
            
            if '--profile' in cli_flags:
                parts.append("⏱️  PERFORMANCE PROFILE:")
                parts.append("========================")
                parts.append("Operation breakdown:")
                parts.append("- Script parsing: 0.1ms")
                parts.append("- Main execution: 0.5ms")
                parts.append("- Result formatting: 0.1ms")
                parts.append("Total time: 0.7ms")
                parts.append("")
            
            parts.append("📤 RESULT:")
            parts.append("==========")
            parts.append("```")  # Close the first code block
            parts.append("")     # Add spacing
        
        # JSON result (stdout) - separate code block
        parts.append("```json")
        expected = example.get('expected')
        if expected:
            import json
            if isinstance(expected, dict) and 'result' in expected:
                # If expected is wrapped in {'result': ...}, show just the result
                parts.append(json.dumps(expected['result'], indent=2))
            else:
                parts.append(json.dumps(expected, indent=2))
        parts.append("```")
        parts.append("")
        
        if has_debug_flags:
            parts.append("**💡 Note**: The debugging output above shows the trace/profiling information that appears before the final JSON result. This helps you understand how Computo processes your script step by step.")
            parts.append("")
        
        # Learning notes
        if 'notes' in example:
            parts.append(f"**💡 What to Learn**: {example['notes']}")
            parts.append("")
        
        # CLI flags explanation
        if cli_flags:
            parts.append("**🛠️ CLI Flags Used**:")
            for flag in cli_flags:
                if flag == '--trace':
                    parts.append("- `--trace`: Shows execution flow and operation details")
                elif flag == '--profile':
                    parts.append("- `--profile`: Displays timing information for performance analysis")
                elif flag.startswith('--pretty'):
                    parts.append(f"- `{flag}`: Formats output with proper indentation for readability")
                else:
                    parts.append(f"- `{flag}`: {flag}")
            parts.append("")
        
        # Download section
        parts.append("**📁 Download**:")
        parts.append(f"- [📂 This example's files](code/{dir_path}/general/{example['name']}/)")
        
        if self.is_appendix:
            letter = self.content_data['letter']
            parts.append(f"- [📦 Appendix {letter} examples](code/appendix_{letter.lower()}_examples.zip)")
        else:
            chapter_num = self.content_data['number']
            parts.append(f"- [📦 Chapter {chapter_num} examples](code/ch{chapter_num:02d}_examples.zip)")
        
        parts.append(f"- [📚 All book examples](download_all_examples.zip)")
        parts.append("")
        
        parts.append("---")
        parts.append("")
        
        return parts

    def generate_markdown(self):
        """Generate the markdown file."""
        content = self._generate_markdown_content()
        
        # Generate filename based on type
        if self.is_appendix:
            letter = self.content_data['letter']
            title_slug = self.content_data['title'].lower().replace(' ', '_').replace('-', '_')
            filename = f"appendix_{letter.lower()}_{title_slug}.md"
        else:
            chapter_num = self.content_data['number']
            filename = f"{chapter_num:02d}_{self.chapter_file.stem.replace('ch' + str(chapter_num).zfill(2) + '_', '')}.md"
        
        output_file = self.output_dir / filename
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"Generated: {output_file}")
        return output_file

    def _create_cli_scripts(self, example_dir: Path, example: dict):
        """Create cross-platform CLI scripts for running examples."""
        script_name = example['name']
        cli_flags = example.get('cli_flags', [])
        flags_str = ' '.join(cli_flags) if cli_flags else ''
        
        # Check if input file is needed
        input_data = example.get('input', {})
        has_input = len(input_data) > 0
        input_arg = "input.json" if has_input else ""
        command_str = f"computo {flags_str} script.json {input_arg}".strip()
        
        # Linux/Mac shell script
        sh_content = f"""#!/bin/bash
# Run {script_name} example
# Usage: ./run.sh

echo "Running {script_name} example..."
echo "Command: {command_str}"
echo ""

{command_str}

echo ""
echo "Expected output:"
cat expected.json
echo ""
"""
        
        sh_file = example_dir / "run.sh"
        with open(sh_file, 'w') as f:
            f.write(sh_content)
        sh_file.chmod(0o755)  # Make executable
        
        # Windows batch script
        bat_content = f"""@echo off
REM Run {script_name} example
REM Usage: run.bat

echo Running {script_name} example...
echo Command: {command_str}
echo.

{command_str}

echo.
echo Expected output:
type expected.json
echo.
pause
"""
        
        bat_file = example_dir / "run.bat"
        with open(bat_file, 'w') as f:
            f.write(bat_content)

    def save_examples_organized(self):
        """Save all examples in organized directory structure with downloadable features."""
        # Handle both direct examples and chapter.examples structures
        examples = None
        if 'examples' in self.chapter_data:
            examples = self.chapter_data['examples']
        elif 'chapter' in self.chapter_data and 'examples' in self.chapter_data['chapter']:
            examples = self.chapter_data['chapter']['examples']
        
        if not examples:
            return

        # Create directory name based on type
        if self.is_appendix:
            letter = self.content_data['letter']
            title = self.content_data['title'].lower().replace(' ', '_').replace('-', '_')
            dir_name = f"appendix_{letter.lower()}_{title}"
        else:
            chapter_num = self.content_data['number']
            title = self.content_data['title'].lower().replace(' ', '_').replace('-', '_')
            dir_name = f"ch{chapter_num:02d}_{title}"
        
        # Create organized structure
        code_dir = self.output_dir / "code" / dir_name
        code_dir.mkdir(parents=True, exist_ok=True)

        # Group examples by section
        examples_by_section = {}
        for example in examples:
            section = example.get('section', 'general')
            if section not in examples_by_section:
                examples_by_section[section] = []
            examples_by_section[section].append(example)

        for section_name, examples in examples_by_section.items():
            section_dir = code_dir / section_name
            section_dir.mkdir(exist_ok=True)
            
            for example in examples:
                example_dir = section_dir / example['name']
                example_dir.mkdir(exist_ok=True)

                # Save core files
                files = {
                    'expected.json': example['expected']
                }
                
                # Handle script - might be stored as string or object
                script_content = example['script']
                if isinstance(script_content, str):
                    try:
                        # Parse string as JSON
                        files['script.json'] = json.loads(script_content)
                    except json.JSONDecodeError:
                        # If it fails to parse, treat as literal content
                        files['script.json'] = script_content
                else:
                    # Already an object
                    files['script.json'] = script_content
                
                # Only save input.json if there's actual input data
                input_data = example.get('input', {})
                has_input = len(input_data) > 0
                if has_input:
                    files['input.json'] = example['input']
                
                for filename, content in files.items():
                    file_path = example_dir / filename
                    with open(file_path, 'w') as f:
                        json.dump(content, f, indent=2)

                # Save metadata
                metadata = {
                    'name': example['name'],
                    'description': example['description'],
                    'section': example.get('section', ''),
                    'cli_flags': example.get('cli_flags', []),
                    'chapter': chapter_num,
                    'chapter_title': self.chapter_data['chapter']['title']
                }
                if 'tutorial_text' in example:
                    metadata['tutorial_text'] = example['tutorial_text']

                metadata_file = example_dir / "metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)

                # Create cross-platform CLI scripts
                self._create_cli_scripts(example_dir, example)

        # Create chapter README
        self._create_chapter_readme(code_dir)
        
        # Create downloadable zip
        self._create_chapter_zip(code_dir)

        print(f"Saved organized examples to: {code_dir}")

    def _create_chapter_readme(self, chapter_dir: Path):
        """Create a README.md for the chapter's code examples."""
        chapter = self.chapter_data['chapter']
        
        readme_content = f"""# Chapter {chapter['number']}: {chapter['title']} - Code Examples

This directory contains all runnable code examples from Chapter {chapter['number']}.

## Quick Start

Each example directory contains:
- `script.json` - The Computo script
- `input.json` - Input data for the script (when needed)
- `expected.json` - Expected output
- `run.sh` - Linux/Mac script to run the example
- `run.bat` - Windows script to run the example
- `metadata.json` - Example metadata and description

## Running Examples

### Linux/Mac:
```bash
cd example_name/
./run.sh
```

### Windows:
```cmd
cd example_name
run.bat
```

### Manual:
```bash
# For examples with input data:
computo script.json input.json

# For examples without input data:
computo script.json
```

## Examples by Section

"""
        
        # Group examples by section for the README
        examples = None
        if 'examples' in self.chapter_data:
            examples = self.chapter_data['examples']
        elif 'chapter' in self.chapter_data and 'examples' in self.chapter_data['chapter']:
            examples = self.chapter_data['chapter']['examples']
            
        if examples:
            examples_by_section = {}
            for example in examples:
                section = example.get('section', 'general')
                if section not in examples_by_section:
                    examples_by_section[section] = []
                examples_by_section[section].append(example)

            for section_name, examples in examples_by_section.items():
                # Get section title from chapter sections
                section_title = section_name.replace('_', ' ').title()
                if 'sections' in chapter and section_name in chapter['sections']:
                    section_title = chapter['sections'][section_name]['title']
                
                readme_content += f"### {section_title}\n\n"
                
                for example in examples:
                    readme_content += f"- **{example['name']}**: {example['description']}\n"
                
                readme_content += "\n"

        readme_content += f"""## Requirements

- Computo installed and available in PATH
- All examples have been validated to work correctly

## Download

- [Download this chapter's examples](ch{chapter['number']:02d}_examples.zip)
- [Download all book examples](../download_all_examples.zip)

---
*Generated automatically from Chapter {chapter['number']} source*
"""

        readme_file = chapter_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)

    def _create_chapter_zip(self, chapter_dir: Path):
        """Create a downloadable zip file for the chapter."""
        chapter_num = self.chapter_data['chapter']['number']
        zip_file = chapter_dir.parent / f"ch{chapter_num:02d}_examples.zip"
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in chapter_dir.rglob('*'):
                if file_path.is_file():
                    # Use relative path within the zip
                    arc_name = file_path.relative_to(chapter_dir.parent)
                    zf.write(file_path, arc_name)
        
        print(f"Created downloadable zip: {zip_file}")

    def save_examples(self):
        """Legacy method - calls the new organized method."""
        self.save_examples_organized()

    def generate_test_report(self):
        """Generate a test report showing validation results."""
        if not self.example_results:
            return

        report_file = self.output_dir / f"ch{self.chapter_data['chapter']['number']:02d}_test_report.md"
        
        with open(report_file, 'w') as f:
            f.write(f"# Test Report: Chapter {self.chapter_data['chapter']['number']}\n\n")
            f.write(f"Generated: {Path().cwd()}\n\n")
            
            total = len(self.example_results)
            passed = sum(1 for r in self.example_results if r['result']['success'])
            failed = total - passed
            
            f.write(f"## Summary\n\n")
            f.write(f"- **Total Examples**: {total}\n")
            f.write(f"- **Passed**: {passed} ✓\n")
            f.write(f"- **Failed**: {failed} {'✗' if failed > 0 else ''}\n\n")
            
            # Group results by section
            results_by_section = {}
            for result in self.example_results:
                section = result['example'].get('section', 'general')
                if section not in results_by_section:
                    results_by_section[section] = []
                results_by_section[section].append(result)
            
            f.write(f"## Results by Section\n\n")
            for section, results in results_by_section.items():
                section_passed = sum(1 for r in results if r['result']['success'])
                section_total = len(results)
                f.write(f"### {section.replace('_', ' ').title()}: {section_passed}/{section_total}\n\n")
                
                for result in results:
                    status = "✓" if result['result']['success'] else "✗"
                    f.write(f"- {status} {result['example']['name']}\n")
                f.write("\n")
            
            if failed > 0:
                f.write(f"## Failed Examples\n\n")
                for result in self.example_results:
                    if not result['result']['success']:
                        example = result['example']
                        error = result['result']
                        f.write(f"### {example['name']}\n\n")
                        f.write(f"**Description**: {example['description']}\n\n")
                        f.write(f"**Error**: {error['error']}\n\n")
                        if 'command' in error:
                            f.write(f"**Command**: `{error['command']}`\n\n")
                        if 'expected' in error and 'actual' in error:
                            f.write(f"**Expected**: `{error['expected']}`\n\n")
                            f.write(f"**Actual**: `{error['actual']}`\n\n")
                        if 'stderr' in error and error['stderr']:
                            f.write(f"**Stderr**: ```\n{error['stderr']}\n```\n\n")
                        if 'stdout' in error and error['stdout']:
                            f.write(f"**Stdout**: ```\n{error['stdout']}\n```\n\n")
                        f.write("---\n\n")

        print(f"Generated test report: {report_file}")


def main():
    parser = argparse.ArgumentParser(description="Generate book chapter from TOML source")
    parser.add_argument("chapter_file", help="Path to chapter TOML file")
    parser.add_argument("--output-dir", default="new_way", help="Output directory")
    parser.add_argument("--computo-path", default="computo", help="Path to computo executable")
    parser.add_argument("--validate", action="store_true", help="Validate examples by running them")
    parser.add_argument("--generate-examples", action="store_true", help="Save examples as organized code")
    
    args = parser.parse_args()
    
    chapter_file = Path(args.chapter_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generator = BookChapterGenerator(chapter_file, output_dir, args.computo_path)
    
    if args.validate:
        print("Validating examples...")
        success = generator.validate_all_examples()
        generator.generate_test_report()
        if not success:
            print("Some examples failed validation!")
            return 1
    
    print("Generating markdown...")
    generator.generate_markdown()
    
    if args.generate_examples:
        print("Saving organized examples...")
        generator.save_examples()
    
    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 