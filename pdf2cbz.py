import argparse
import fitz  # PyMuPDF
from PIL import Image
import io
import zipfile
import os
import sys

def convert_to_cbz(pdf_path, cbz_path, image_format="webp", quality=80):
    """Converts a PDF to a CBZ archive, optionally using WebP images for compression.

    Args:
        pdf_path (str): Path to the input PDF file.
        cbz_path (str): Path to the output CBZ file.
        image_format (str, optional): Image format to use for individual pages.
            Choices: 'png', 'webp'. Defaults to 'webp'.
        quality (int, optional): Compression quality for WebP images (1-100). Defaults to 80.

    Raises:
        ValueError: If `image_format` is not `'png'` or `'webp'`.
    """

    if image_format not in ("png", "webp"):
        raise ValueError("Unsupported image format. Choose 'png' or 'webp'.")

    doc = fitz.open(pdf_path)
    with zipfile.ZipFile(cbz_path, 'w') as cbz:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()

            # Extract page content efficiently as PIL Image
            img = pix.pil_image.convert('RGB')  # Ensure correct color mode

            # Optionally apply compression (with PIL's built-in WebP support)
            if image_format == "webp":
                webp_bytes = io.BytesIO()
                img.save(webp_bytes, format="WEBP", quality=quality)
                img_bytes = webp_bytes.getvalue()
            else:
                img_bytes = img.tobytes("png")

            img_filename = f"page_{page_num + 1}.{image_format}"
            cbz.writestr(img_filename, img_bytes)

    doc.close()
    print(f"Conversion complete. The CBZ archive is saved as {cbz_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to CBZ.")
    parser.add_argument("--input", "-i", required=True, help="Input PDF file")
    parser.add_argument("--output", "-o", required=True, help="Output CBZ file")
    parser.add_argument("--format", "-f", choices=["png", "webp"], default="webp", help="Image format (default: webp)")
    parser.add_argument("--quality", "-q", type=int, choices=range(1, 101), default=80, help="WebP compression quality (1-100)")
    args = parser.parse_args()

    # Perform the conversion with error handling and informative output
    try:
        convert_to_cbz(args.input, args.output, args.format, args.quality)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()