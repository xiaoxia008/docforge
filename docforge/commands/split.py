"""PDF 拆分功能模块"""

import os

import click
from pypdf import PdfReader, PdfWriter
from rich.console import Console

from docforge.utils import ensure_output_dir, handle_error, validate_pdf

console = Console()


@click.command("split")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--pages", "-p", default=None, help="页码范围，如 1-5 或 3,5,7")
@click.option("--each", is_flag=True, help="每页拆分为单独的 PDF")
@click.option("-o", "--output", default="output", help="输出目录或文件路径")
def split(input_file, pages, each, output):
    """拆分 PDF 文件。

    示例:
        docforge split input.pdf --pages 1-5 -o output.pdf
        docforge split input.pdf --each -o output_dir/
    """
    try:
        if not validate_pdf(input_file):
            raise SystemExit(1)

        reader = PdfReader(input_file)
        total_pages = len(reader.pages)

        if each:
            # If output ends with / or doesn't end with .pdf, treat as directory
            if output.endswith("/") or not output.lower().endswith(".pdf"):
                output_dir = output
            else:
                # User gave a file path, use its parent directory
                output_dir = os.path.dirname(output) or "split_output"
            ensure_output_dir(output_dir)
            base_name = os.path.splitext(os.path.basename(input_file))[0]

            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                out_path = os.path.join(output_dir, f"{base_name}_page_{i + 1}.pdf")
                with open(out_path, "wb") as f:
                    writer.write(f)

            console.print(f"[green]✓ 拆分成功！共 {total_pages} 页，输出目录：{output_dir}[/green]")

        elif pages:
            page_indices = _parse_page_range(pages, total_pages)
            ensure_output_dir(output)
            writer = PdfWriter()

            for idx in page_indices:
                writer.add_page(reader.pages[idx])

            with open(output, "wb") as f:
                writer.write(f)

            console.print(f"[green]✓ 拆分成功！提取了 {len(page_indices)} 页，输出：{output}[/green]")

        else:
            console.print("[red]错误：请指定 --pages 或 --each 参数[/red]")
            raise SystemExit(1)

    except SystemExit:
        raise
    except Exception as e:
        handle_error(e, "PDF 拆分失败")


def _parse_page_range(pages_str: str, total_pages: int) -> list:
    """解析页码范围字符串。

    Args:
        pages_str: 页码范围字符串，如 "1-5" 或 "3,5,7"。
        total_pages: PDF 总页数。

    Returns:
        页码索引列表（0-based）。
    """
    indices = set()
    parts = pages_str.split(",")

    for part in parts:
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = int(start.strip())
            end = int(end.strip())
            if start < 1 or end > total_pages:
                raise ValueError(f"页码范围超出范围：{part}（总页数：{total_pages}）")
            for p in range(start, end + 1):
                indices.add(p - 1)
        else:
            p = int(part)
            if p < 1 or p > total_pages:
                raise ValueError(f"页码超出范围：{p}（总页数：{total_pages}）")
            indices.add(p - 1)

    return sorted(indices)
