# PDF to CBZ Converter (and Vice-Versa)

A robust tool to convert PDF files to CBZ (Comic Book Archive) format and vice-versa. Perfect for optimizing comics, manga, and magazines for e-readers and comic apps.

## Features

*   **Bidirectional Conversion:** Convert PDF -> CBZ and CBZ/ZIP -> PDF.
*   **WebP Support:** Full support for WebP images in both directions (even when comic readers/PyMuPDF don't support it natively).
*   **Batch Processing:** Process entire directories of files at once.
*   **Multiprocessing:** Utilizes multiple CPU cores for fast batch conversion.
*   **Smart Metadata:** 
    *   **PDF -> CBZ:** Automatically extracts PDF metadata and generates `ComicInfo.xml`.
    *   **CBZ -> PDF:** Extracts metadata from `ComicInfo.xml` and embeds it into the resulting PDF.
*   **Image Optimization:**
    *   **Format:** Choose between WebP (default, smaller) or PNG (lossless).
    *   **Quality:** Adjust WebP compression quality.
    *   **DPI/Resolution:** Downscale or upscale images (e.g., for specific device screens).
    *   **Grayscale:** Convert to grayscale for E-Ink devices.
*   **Correct Sorting:** Zero-padded filenames ensure pages read in the correct order.

## Local Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/youruser/pdf2cbz.git
    cd pdf2cbz
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Basic Conversion
```bash
# Convert PDF to CBZ
python3 pdf2cbz.py -i input.pdf

# Convert CBZ to PDF
python3 pdf2cbz.py -i comic.cbz
```

### Batch Processing
Convert all PDFs in a folder to CBZ:
```bash
python3 pdf2cbz.py -i /path/to/comics/ -o /path/to/output/
```

### Advanced Options
```bash
# optimize for an old tablet (low resolution, grayscale)
python3 pdf2cbz.py -i input.pdf -o output.cbz --dpi 150 --grayscale --quality 60
```

### Arguments

*   `-i`, `--input`: Input file or directory (PDF, CBZ, ZIP).
*   `-o`, `--output`: Output file or directory (optional).
*   `-f`, `--format`: Image format inside CBZ (`webp` or `png`). Default: `webp`.
*   `-q`, `--quality`: WebP quality (1-100). Default: 80.
*   `-d`, `--dpi`: Target DPI for PDF conversion (e.g., 150, 300).
*   `-g`, `--grayscale`: Convert images to grayscale.
*   `-w`, `--workers`: Number of worker processes for batch mode.

## Docker Usage

You can also run `pdf2cbz` using Docker, which avoids installing dependencies on your host machine.

### Prerequisites
*   Docker
*   Docker Compose

### Setup
1.  Build the image:
    ```bash
    docker-compose build
    ```
2.  Place your input files (PDF or CBZ) in the `data/` directory.

### Running
Run the tool using `docker-compose run`. Map the `data` folder to access your files.

**Basic Example:**
```bash
docker-compose run --rm pdf2cbz -i /data/my_comic.pdf
```

## Development

### Testing
Run the test suite:
```bash
PYTHONPATH=. pytest tests/
```

### Linting
Check for code style:
```bash
flake8 pdf2cbz.py
```
