import os
import sys
from collections import defaultdict

def generate_html_with_pdf_links(output_filename=None, interactive_mode=False, use_headers=False):
    # Helper function to validate filenames
    def validate_filename(filename):
        invalid_chars = r'<>:"/\|?*'
        for char in invalid_chars:
            if char in filename:
                return False
        return True

    # Function to get file name without path and extension
    def get_clean_file_name(file_path):
        return os.path.splitext(os.path.basename(file_path))[0]

    # Ask for output filename if not provided
    if not output_filename:
        output_filename = input("Enter the name for the output HTML file (default: pdf_links.html): ").strip()
        if not output_filename:
            output_filename = "pdf_links.html"  # Default name
        if not validate_filename(output_filename):
            print("Invalid filename. Please avoid special characters like <>:\"/\\|?*")
            return

    # Normalize output filename path
    output_filename = os.path.normpath(output_filename)

    # Get the current working directory
    current_dir = os.getcwd()

    # Dictionary to store PDF files grouped by subfolder
    grouped_pdfs = defaultdict(list)

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                # Create a relative path for the file
                relative_path = os.path.relpath(os.path.join(root, file), current_dir)

                # Get the subfolder name
                subfolder = os.path.relpath(root, current_dir) if root != current_dir else "."

                # Interactive mode: ask the user about each file
                if interactive_mode:
                    print(f"Found: {relative_path}")
                    include_file = input("Do you want to add this file to the HTML? (press Enter to add, type 'n' to skip): ").strip().lower()
                    if include_file == 'n':
                        print(f"Skipping: {relative_path}")
                        continue
                    display_name = input(
                        "Enter the display name for this file (default: file name without extension): ").strip()
                    if not display_name:
                        display_name = get_clean_file_name(file)
                else:
                    display_name = get_clean_file_name(file)  # Default to file name without extension

                # Add to the grouped dictionary
                grouped_pdfs[subfolder].append((relative_path, display_name))
                print(f"Link for {relative_path} has been successfully created!")

    # Check if there are any PDF files to add
    if not any(grouped_pdfs.values()):
        print("No PDF files found or selected to add to the HTML.")
        return

    # Generate the HTML content
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Links</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>List of PDF Files</h1>
"""

    # Add links grouped by subfolder (if `use_headers` is enabled)
    for subfolder, files in grouped_pdfs.items():
        if use_headers and subfolder != ".":
            html_content += f"    <h2>{subfolder}</h2>\n"
        html_content += "    <ul>\n"
        for relative_path, display_name in files:
            html_content += f'        <li><a href="{relative_path}" target="_blank" title="{display_name}">{display_name}</a></li>\n'
        html_content += "    </ul>\n"

    html_content += """</body>
</html>
"""

    # Write the HTML content to the output file
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"\nHTML document generated: {output_filename}")
    except Exception as e:
        print(f"Error writing to file {output_filename}: {e}")

# Run the script
if __name__ == "__main__":
    # Check for command-line arguments
    output_file = None
    interactive_mode = False
    use_headers = False

    # Parse arguments
    for arg in sys.argv[1:]:
        if arg == "-i":
            interactive_mode = True
        elif arg == "-h":
            use_headers = True
        else:
            output_file = arg

    generate_html_with_pdf_links(output_file, interactive_mode, use_headers)

