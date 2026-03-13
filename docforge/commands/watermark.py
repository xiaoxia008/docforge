"""PDF 水印功能模块 - 使用 pypdf 实现，避免 reportlab 兼容性问题"""

import os
import tempfile

import click
from pypdf import PdfReader, PdfWriter
from rich.console import Console

from docforge.utils import ensure_output_dir, handle_error, validate_pdf

console = Console()


@click.command("watermark")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--text", "-t", default=None, help="水印文字内容")
@click.option("--image", "-i", default=None, type=click.Path(exists=True), help="水印图片路径")
@click.option("-o", "--output", default=None, help="输出文件路径")
@click.option(
    "--opacity",
    default=0.3,
    type=float,
    help="水印透明度 (0.0-1.0)",
    show_default=True,
)
def watermark(input_file, text, image, output, opacity):
    """给 PDF 添加文字或图片水印。

    示例:
        docforge watermark input.pdf --text "CONFIDENTIAL" -o output.pdf
        docforge watermark input.pdf --image logo.png -o output.pdf
    """
    try:
        if not validate_pdf(input_file):
            raise SystemExit(1)

        if not text and not image:
            console.print("[red]错误：请指定 --text 或 --image 参数[/red]")
            raise SystemExit(1)

        if text and image:
            console.print("[red]错误：--text 和 --image 不能同时使用[/red]")
            raise SystemExit(1)

        if output is None:
            base, ext = input_file.rsplit(".", 1)
            output = f"{base}_watermarked.{ext}"

        ensure_output_dir(output)

        reader = PdfReader(input_file)
        writer = PdfWriter()

        if text:
            watermark_pdf_path = _create_text_watermark_pypdf(text, reader.pages[0])
        else:
            watermark_pdf_path = _create_image_watermark_pypdf(image, opacity, reader.pages[0])

        watermark_reader = PdfReader(watermark_pdf_path)
        watermark_page = watermark_reader.pages[0]

        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)

        with open(output, "wb") as f:
            writer.write(f)

        # Clean up temp file
        try:
            os.unlink(watermark_pdf_path)
        except Exception:
            pass

        watermark_type = f"文字「{text}」" if text else f"图片「{image}」"
        console.print(f"[green]✓ 水印添加成功！{watermark_type}，输出：{output}[/green]")

    except Exception as e:
        handle_error(e, "水印添加失败")


def _create_text_watermark_pypdf(text: str, sample_page) -> str:
    """使用 SVG + pypdf 创建文字水印。

    通过创建一个包含 SVG 渲染文字的 PDF 作为水印。

    Args:
        text: 水印文字。
        sample_page: 用于获取页面尺寸的示例页面。

    Returns:
        水印 PDF 临时文件路径。
    """
    try:
        page_width = float(sample_page.mediabox.width)
        page_height = float(sample_page.mediabox.height)
    except Exception:
        page_width, page_height = 595, 842  # A4 default

    # Create a simple PDF with text using fpdf2 (no reportlab dependency)
    from fpdf import FPDF

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 40)
    pdf.set_text_color(128, 128, 128)  # Gray

    # Add text watermark
    pdf.text(page_width / 2 - 50, page_height / 2, text)

    pdf.output(tmp.name)
    return tmp.name


def _create_image_watermark_pypdf(image_path: str, opacity: float, sample_page) -> str:
    """使用 Pillow + fpdf2 创建图片水印。

    Args:
        image_path: 水印图片路径。
        opacity: 透明度。
        sample_page: 用于获取页面尺寸的示例页面。

    Returns:
        水印 PDF 临时文件路径。
    """
    from PIL import Image as PILImage
    from fpdf import FPDF

    try:
        page_width = float(sample_page.mediabox.width)
        page_height = float(sample_page.mediabox.height)
    except Exception:
        page_width, page_height = 595, 842

    img = PILImage.open(image_path)

    # Apply opacity to image
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Create transparent version
    alpha = img.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    img.putalpha(alpha)

    # Save temporary transparent image
    tmp_img = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp_img.close()
    img.save(tmp_img.name, "PNG")

    # Calculate centered position
    img_width, img_height = img.size
    scale = min(page_width / img_width, page_height / img_height) * 0.5
    draw_width = img_width * scale
    draw_height = img_height * scale
    x = (page_width - draw_width) / 2
    y = (page_height - draw_height) / 2

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.image(tmp_img.name, x=x, y=y, w=draw_width, h=draw_height)
    pdf.output(tmp.name)

    # Clean up temp image
    try:
        os.unlink(tmp_img.name)
    except Exception:
        pass

    return tmp.name
