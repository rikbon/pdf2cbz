import os
import zipfile
import io
import fitz
from PIL import Image
import pytest
from pdf2cbz import convert_pdf_to_cbz, convert_cbz_to_pdf

def test_pdf_to_cbz(tmp_path):
    # Create a simple PDF
    pdf_path = tmp_path / "test.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Test Page")
    doc.save(str(pdf_path))
    doc.close()
    
    cbz_path = tmp_path / "test.cbz"
    convert_pdf_to_cbz(str(pdf_path), str(cbz_path), image_format="png")
    
    assert cbz_path.exists()
    with zipfile.ZipFile(cbz_path, 'r') as cbz:
        assert "page_1.png" in cbz.namelist()
        assert "ComicInfo.xml" in cbz.namelist()

def test_cbz_to_pdf_webp(tmp_path):
    # Create a CBZ with WebP image
    cbz_path = tmp_path / "test_webp.cbz"
    with zipfile.ZipFile(cbz_path, 'w') as cbz:
        img = Image.new('RGB', (100, 100), color=(255, 0, 0))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="WEBP")
        cbz.writestr("page_1.webp", img_buffer.getvalue())
        
        comic_info = '<ComicInfo><Title>Test Title</Title></ComicInfo>'
        cbz.writestr("ComicInfo.xml", comic_info)
    
    pdf_path = tmp_path / "test_webp.pdf"
    convert_cbz_to_pdf(str(cbz_path), str(pdf_path))
    
    assert pdf_path.exists()
    doc = fitz.open(str(pdf_path))
    assert len(doc) == 1
    assert doc.metadata["title"] == "Test Title"
    doc.close()

def test_batch_processing(tmp_path):
    # Create multiple PDFs
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    for i in range(3):
        pdf_path = input_dir / f"test_{i}.pdf"
        doc = fitz.open()
        doc.new_page()
        doc.save(str(pdf_path))
        doc.close()
    
    # Run main logic for batch
    # Since main() uses argparse, we can just test the process_file function
    from pdf2cbz import process_file
    class Args:
        format = "webp"
        quality = 80
        dpi = None
        grayscale = False
    
    args = Args()
    for i in range(3):
        input_path = str(input_dir / f"test_{i}.pdf")
        output_path = str(input_dir / f"test_{i}.cbz")
        result = process_file((input_path, output_path, args))
        assert "Successfully" in result
        assert os.path.exists(output_path)
