# PDF to CBZ Converter (and Vice-Versa)

A robust tool to convert PDF files to CBZ (Comic Book Archive) format and vice-versa. Perfect for optimizing comics, manga, and magazines for e-readers and comic apps.

## Features

*   **Bidirectional Conversion:** Convert PDF -> CBZ and CBZ/ZIP -> PDF.
*   **Batch Processing:** Process entire directories of files at once.
*   **Multiprocessing:** Utilizes multiple CPU cores for fast batch conversion.
*   **Smart Metadata:** Automatically extracts PDF metadata and generates `ComicInfo.xml` for comic readers.
*   **Image Optimization:**
    *   **Format:** Choose between WebP (default, smaller) or PNG (lossless).
    *   **Quality:** Adjust WebP compression quality.
    *   **DPI/Resolution:** Downscale or upscale images (e.g., for specific device screens).
    *   **Grayscale:** Convert to grayscale for E-Ink devices.
*   **Correct Sorting:** Zero-padded filenames ensure pages read in the correct order.

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
# Convert a PDF located in the ./data folder
docker-compose run --rm pdf2cbz -i /data/my_comic.pdf
```

**Batch Processing:**
```bash
# Process all files in the data directory
docker-compose run --rm pdf2cbz -i /data
```

**Advanced Options:**
```bash
docker-compose run --rm pdf2cbz -i /data/manga.pdf --grayscale --dpi 300
```


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
python3 pdf2cbz.py -i /path/to/comics/
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
