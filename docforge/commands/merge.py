"""PDF 合并功能模块"""

import click
from pypdf import PdfReader, PdfWriter
from rich.console import Console
from rich.progress import track

from docforge.utils import ensure_output_dir, get_file_size_str, handle_error

console = Console()


@click.command("merge")
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("-o", "--output", default="merged.pdf", help="输出文件路径", show_default=True)
def merge(files, output):
    """合并多个 PDF 文件为一个。

    示例:
        docforge merge file1.pdf file2.pdf -o output.pdf
        docforge merge *.pdf -o combined.pdf
    """
    try:
        if len(files) < 2:
            console.print("[red]错误：至少需要两个 PDF 文件进行合并[/red]")
            raise SystemExit(1)

        ensure_output_dir(output)
        writer = PdfWriter()

        for file_path in track(files, description="[cyan]正在合并...[/cyan]"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                writer.add_page(page)

        with open(output, "wb") as f:
            writer.write(f)

        size_str = get_file_size_str(output)
        console.print(f"[green]✓ 合并成功！共合并 {len(files)} 个文件，输出：{output} ({size_str})[/green]")

    except Exception as e:
        handle_error(e, "PDF 合并失败")
