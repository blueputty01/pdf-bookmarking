# Automated PDF Bookmarking Tool 🔖

This is a tool to automatically generate bookmarks for PDF files given a formatted list of bookmarks in plain text.

## Usage instructions

Designed to add bookmarks given a nested lit of bookmarks in the following format:

```text
Chapter 1
    Section 1.1
    Section 1.2
Chapter 2
    Section 2.1
        Subsection 2.1.1
        Subsection 2.1.2
    Section 2.2
```

```bash
python main.py
```

Each indentation level must be denoted with leading group(s) of 2 spaces. This is configurable in the script.

The tool will automatically generate bookmarks for each line, and will nest them appropriately.

## Other

This repo also contains nice utility tools like page extraction and OCR.
