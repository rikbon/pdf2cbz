# pdf2cbz

Convert PDF files to CBZ (Comic Book Zip) format with ease, leveraging the power of Python. This tool provides a seamless way to transform your PDFs into CBZ archives, ideal for comic book enthusiasts and digital archivists alike. 

## Features

- Convert PDF to CBZ archive.
- Option to use WebP for image compression, offering high-quality images at smaller file sizes.
- Customizable image quality settings.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### Using Conda

If you prefer using Conda, follow these steps to create a new environment and install the required dependencies:

1. Create a new Conda environment:
   ```shell
   conda create --name pdf2cbz python=3.8
   ```
2. Activate the environment:
   ```shell
   conda activate pdf2cbz
   ```
3. Install the dependencies:
   ```shell
   conda install -c conda-forge pymupdf pillow
   ```

### Using Python's Virtual Environment

For those who prefer Python's virtual environment, follow these steps:

1. Create a virtual environment:
   ```shell
   python3 -m venv pdf2cbz-env
   ```
2. Activate the environment:
   For Windows:
   ```shell
   pdf2cbz-env\Scripts\activate
   ```
   For Unix or MacOS:
   ```shell
   source pdf2cbz-env/bin/activate
   ```
3. Install the dependencies from `requirements.txt`:
   ```shell
   pip install -r requirements.txt
   ```

## Usage

To convert a PDF to CBZ format, run the `pdf2cbz.py` script with the following command:

```shell
python pdf2cbz.py --input <path_to_pdf> --output <path_to_cbz> --format <image_format> --quality <quality>
```

- `<path_to_pdf>`: Path to the source PDF file.
- `<path_to_cbz>`: Path to the output CBZ file.
- `<image_format>`: (Optional) Image format for compression. Choose between 'png' and 'webp'. Default is 'webp'.
- `<quality>`: (Optional) Quality of the compressed images. Default is 80.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.