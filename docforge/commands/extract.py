"""PDF 文字提取功能模块"""

import click
from pypdf import PdfReader
from rich.console import Console

from docforge.utils import ensure_output_dir, handle_error, validate_pdf

console = Console()


@click.command("extract")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", default=None, help="输出文件路径")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "markdown"]),
    default="text",
    help="输出格式",
    show_default=True,
)
def extract(input_file, output, output_format):
    """从 PDF 提取文字内容。

    示例:
        docforge extract input.pdf -o output.txt
        docforge extract input.pdf --format markdown -o output.md
    """
    try:
        if not validate_pdf(input_file):
            raise SystemExit(1)

        reader = PdfReader(input_file)
        total_pages = len(reader.pages)

        if output is None:
            ext = "md" if output_format == "markdown" else "txt"
            output = input_file.rsplit(".", 1)[0] + f".{ext}"

        ensure_output_dir(output)

        lines = []
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            if output_format == "markdown":
                lines.append(f"## 第 {i} 页\n")
                lines.append(text.strip())
                lines.append("\n")
            else:
                lines.append(f"--- 第 {i} 页 ---")
                lines.append(text.strip())
                lines.append("")

        content = "\n".join(lines)
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)

        char_count = len(content)
        console.print(
            f"[green]✓ 提取成功！共 {total_pages} 页，{char_count} 字符，输出：{output}[/green]"
        )

    except Exception as e:
        handle_error(e, "文字提取失败")
