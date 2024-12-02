# PDF Link Generator

This Python script generates an HTML document containing links to all PDF files found in the current directory and its subdirectories. It offers options for interactive mode and grouping files by subfolder for better organization.

## Features

1. Automatically scans the current directory and subdirectories for PDF files.
2. Generates an HTML file with clickable links to each PDF.
3. **Interactive Mode (`-i`)**: Prompts the user to decide which files to include and specify custom link names.
4. **Group by Subfolder (`-h`)**: Organizes links into sections based on subfolder names.
5. Default behavior: Adds all PDF files with link names based on the file names (excluding extensions).

## Requirements

- Python 3.6 or newer

## Installation

No external libraries are required. Just download or copy the script into your working directory.

## Usage

Run the script from the command line:

```bash
python generate_pdf_links.py [output_file] [-i] [-h]

