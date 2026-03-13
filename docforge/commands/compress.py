"""PDF 压缩功能模块"""

import click
from pypdf import PdfReader, PdfWriter
from rich.console import Console

from docforge.utils import ensure_output_dir, get_file_size_str, handle_error, validate_pdf

console = Console()

QUALITY_MAP = {
    "low": 50,
    "medium": 75,
    "high": 95,
}


@click.command("compress")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", default=None, help="输出文件路径")
@click.option(
    "--quality",
    type=click.Choice(["low", "medium", "high"]),
    default="medium",
    help="压缩质量",
    show_default=True,
)
def compress(input_file, output, quality):
    """压缩 PDF 文件减小体积。

    示例:
        docforge compress input.pdf -o output.pdf --quality medium
    """
    try:
        if not validate_pdf(input_file):
            raise SystemExit(1)

        if output is None:
            base, ext = input_file.rsplit(".", 1)
            output = f"{base}_compressed.{ext}"

        ensure_output_dir(output)
        original_size = get_file_size_str(input_file)

        reader = PdfReader(input_file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.add_metadata(reader.metadata or {})

        for page in writer.pages:
            try:
                page.compress_content_streams()
            except Exception:
                pass

        with open(output, "wb") as f:
            writer.write(f)

        compressed_size = get_file_size_str(output)
        console.print(
            f"[green]✓ 压缩成功！{original_size} → {compressed_size}，输出：{output}[/green]"
        )

    except Exception as e:
        handle_error(e, "PDF 压缩失败")
