import os
import markdown

# --- Configuration ---
# Source files to convert
SOURCE_FILES = [
    "README.md",
    "docs/SYLLABUS.md",
    "docs/REQUISITOS.md",
    "docs/BIBLIOGRAFIA.md",
    "docs/RUBRICAS.md",
    "asignaciones/reto1_instrucciones.md",
    "asignaciones/reto2_instrucciones.md",
    "asignaciones/reto3_instrucciones.md",
]

# Output directory for generated HTML
OUTPUT_DIR = "website/pages"

# HTML template for wrapping the content
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <div class="content">
        {content}
    </div>
</body>
</html>
"""

# --- Build Script ---
def build():
    """Converts specified markdown files to HTML."""
    print(f"Creating output directory: {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for md_file_path in SOURCE_FILES:
        try:
            print(f"Processing {md_file_path}...")
            with open(md_file_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            # Convert markdown to HTML
            html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

            # Wrap in full HTML template
            final_html = HTML_TEMPLATE.format(content=html_content)

            # Determine output path
            base_name = os.path.basename(md_file_path).replace(".md", ".html")
            output_path = os.path.join(OUTPUT_DIR, base_name)

            # Save the generated HTML
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_html)
            print(f"  -> Saved to {output_path}")

        except FileNotFoundError:
            print(f"  [!] Warning: File not found, skipping: {md_file_path}")
        except Exception as e:
            print(f"  [!] Error processing {md_file_path}: {e}")

    print("\nBuild finished successfully!")

if __name__ == "__main__":
    build()
