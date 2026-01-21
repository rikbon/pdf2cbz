import argparse
import fitz  # PyMuPDF
from PIL import Image
import io
import zipfile
import os
import sys

import xml.etree.ElementTree as ET

def generate_comic_info(metadata):
    """Generates ComicInfo.xml content from PDF metadata."""
    root = ET.Element("ComicInfo")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

    if metadata.get("title"):
        ET.SubElement(root, "Title").text = metadata["title"]
    if metadata.get("author"):
        ET.SubElement(root, "Writer").text = metadata["author"]
    if metadata.get("subject"):
        ET.SubElement(root, "Summary").text = metadata["subject"]
    
    # Generate pretty XML string
    # Python's xml.etree doesn't do pretty printing easily in older versions, 
    # but we can just write the string.
    try:
        xml_str = ET.tostring(root, encoding="utf-8", method="xml")
        return xml_str
    except Exception:
        return None

def convert_pdf_to_cbz(pdf_path, cbz_path, image_format="webp", quality=80, dpi=None, grayscale=False):
    """Converts a PDF to a CBZ archive."""
    if image_format not in ("png", "webp"):
        raise ValueError("Unsupported image format. Choose 'png' or 'webp'.")

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    num_digits = len(str(total_pages))

    # Calculate matrix for DPI if provided
    matrix = fitz.Matrix(dpi / 72, dpi / 72) if dpi else fitz.Identity

    with zipfile.ZipFile(cbz_path, 'w') as cbz:
        # Write ComicInfo.xml
        xml_data = generate_comic_info(doc.metadata)
        if xml_data:
            cbz.writestr("ComicInfo.xml", xml_data)

        for page_num in range(total_pages):
            print(f"Processing page {page_num + 1}/{total_pages}...", end='\r', flush=True)

            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=matrix)
            
            # Use method call for pil_image()
            img = pix.pil_image().convert('RGB')
            
            if grayscale:
                img = img.convert('L')

            img_buffer = io.BytesIO()
            if image_format == "webp":
                img.save(img_buffer, format="WEBP", quality=quality)
            else:
                img.save(img_buffer, format="PNG")
            
            img_bytes = img_buffer.getvalue()
            img_filename = f"page_{page_num + 1:0{num_digits}d}.{image_format}"
            cbz.writestr(img_filename, img_bytes)

    doc.close()
    print(f"\nConversion complete: {cbz_path}")

# ... (convert_cbz_to_pdf remains unchanged)

import concurrent.futures

# ... (Previous imports and functions)

def process_file(file_info):
    """Wrapper for processing a single file, suitable for multiprocessing."""
    input_path, output_path, args = file_info
    
    # Re-import fitz inside process for safety if needed (though usually fine with fork)
    # Determine mode
    ext = os.path.splitext(input_path)[1].lower()
    try:
        if ext == ".pdf":
            convert_pdf_to_cbz(input_path, output_path, args.format, args.quality, args.dpi, args.grayscale)
        elif ext in (".cbz", ".zip"):
            convert_cbz_to_pdf(input_path, output_path)
        return f"Successfully processed: {input_path}"
    except Exception as e:
        return f"Error processing {input_path}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to CBZ and vice-versa.")
    parser.add_argument("--input", "-i", required=True, help="Input file or directory")
    parser.add_argument("--output", "-o", help="Output file or directory (optional)")
    parser.add_argument("--format", "-f", choices=["png", "webp"], default="webp", help="Image format for CBZ output (default: webp)")
    parser.add_argument("--quality", "-q", type=int, choices=range(1, 101), default=80, help="WebP compression quality (1-100)")
    parser.add_argument("--dpi", "-d", type=int, help="Output DPI for PDF->CBZ (default: PDF native resolution)")
    parser.add_argument("--grayscale", "-g", action="store_true", help="Convert images to grayscale (PDF->CBZ only)")
    parser.add_argument("--workers", "-w", type=int, default=os.cpu_count(), help="Number of worker processes for batch mode")
    
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    tasks = []

    if os.path.isdir(input_path):
        # Batch mode
        if output_path and not os.path.exists(output_path):
            os.makedirs(output_path)
        
        for root, _, files in os.walk(input_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in (".pdf", ".cbz", ".zip"):
                    file_in = os.path.join(root, file)
                    
                    # Determine output filename
                    if output_path:
                        # If output dir specified, flatten structure or keep? Flattening is simpler for now.
                        # Actually, let's keep it simple: output to output_dir with new extension
                        base_name = os.path.splitext(file)[0]
                        new_ext = ".cbz" if ext == ".pdf" else ".pdf"
                        file_out = os.path.join(output_path, base_name + new_ext)
                    else:
                        # Output in same directory
                        new_ext = ".cbz" if ext == ".pdf" else ".pdf"
                        file_out = os.path.splitext(file_in)[0] + new_ext
                    
                    tasks.append((file_in, file_out, args))
    
    elif os.path.exists(input_path):
        # Single file mode
        ext = os.path.splitext(input_path)[1].lower()
        if ext in (".pdf", ".cbz", ".zip"):
            if not output_path:
                new_ext = ".cbz" if ext == ".pdf" else ".pdf"
                output_path = os.path.splitext(input_path)[0] + new_ext
            tasks.append((input_path, output_path, args))
        else:
             print(f"Error: Unsupported file extension '{ext}'.")
             sys.exit(1)
    else:
        print(f"Error: Input '{input_path}' not found.")
        sys.exit(1)

    if not tasks:
        print("No valid files found to process.")
        sys.exit(0)

    print(f"Found {len(tasks)} file(s) to process.")
    
    # Use ProcessPoolExecutor for parallel processing
    # Note: max_workers=1 if only 1 task to avoid overhead, or just use serial
    if len(tasks) == 1:
        print(process_file(tasks[0]))
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(process_file, task) for task in tasks]
            for future in concurrent.futures.as_completed(futures):
                print(future.result())

if __name__ == "__main__":
    main()
