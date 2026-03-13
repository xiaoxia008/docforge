"""PDF 水印功能模块"""

import click
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    ContentStream,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
    TextStringObject,
)
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
            watermark_pdf = _create_text_watermark(text, opacity, reader.pages[0])
        else:
            watermark_pdf = _create_image_watermark(image, opacity)

        watermark_reader = PdfReader(watermark_pdf)
        watermark_page = watermark_reader.pages[0]

        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)

        with open(output, "wb") as f:
            writer.write(f)

        watermark_type = f"文字「{text}」" if text else f"图片「{image}」"
        console.print(f"[green]✓ 水印添加成功！{watermark_type}，输出：{output}[/green]")

    except Exception as e:
        handle_error(e, "水印添加失败")


def _create_text_watermark(text: str, opacity: float, sample_page) -> str:
    """创建文字水印 PDF。

    Args:
        text: 水印文字。
        opacity: 透明度。
        sample_page: 用于获取页面尺寸的示例页面。

    Returns:
        水印 PDF 临时文件路径。
    """
    import io

    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    try:
        page_width = float(sample_page.mediabox.width)
        page_height = float(sample_page.mediabox.height)
    except Exception:
        page_width, page_height = letter

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    c.saveState()
    c.setFillAlpha(opacity)
    c.setFont("Helvetica", 40)

    c.translate(page_width / 2, page_height / 2)
    c.rotate(45)

    c.drawCentredString(0, 0, text)

    c.restoreState()
    c.save()

    packet.seek(0)
    return packet


def _create_image_watermark(image_path: str, opacity: float) -> str:
    """创建图片水印 PDF。

    Args:
        image_path: 水印图片路径。
        opacity: 透明度。

    Returns:
        水印 PDF 临时文件路径。
    """
    import io

    from PIL import Image as PILImage
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    img = PILImage.open(image_path)
    img_width, img_height = img.size

    page_width, page_height = letter
    scale = min(page_width / img_width, page_height / img_height) * 0.5
    draw_width = img_width * scale
    draw_height = img_height * scale

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    c.saveState()
    c.setFillAlpha(opacity)
    c.drawImage(
        image_path,
        (page_width - draw_width) / 2,
        (page_height - draw_height) / 2,
        width=draw_width,
        height=draw_height,
        mask="auto",
    )
    c.restoreState()
    c.save()

    packet.seek(0)
    return packet
