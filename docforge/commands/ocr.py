"""OCR 命令 - 从扫描件 PDF 提取文字"""

import os

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from docforge.utils import ensure_output_dir, handle_error, validate_pdf

console = Console()


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", help="输出文件路径")
@click.option(
    "--lang",
    default="chi_sim+eng",
    help="OCR 语言 (默认: chi_sim+eng 中文+英文)",
)
@click.option(
    "--dpi",
    default=300,
    help="图片分辨率 (默认: 300)",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "markdown"]),
    default="text",
    help="输出格式 (默认: text)",
)
def ocr(input_file, output, lang, dpi, output_format):
    """从扫描件 PDF 提取文字 (OCR)。

    示例:

    \b
        docforge ocr scanned.pdf -o output.txt
        docforge ocr scanned.pdf --lang chi_sim -o output.txt
        docforge ocr scanned.pdf --format markdown -o output.md
    """
    if not os.path.exists(input_file):
        console.print(f"[red]✗[/red] 文件不存在: {input_file}")
        raise SystemExit(1)

    if not output:
        base = os.path.splitext(input_file)[0]
        ext = ".md" if output_format == "markdown" else ".txt"
        output = f"{base}_ocr{ext}"

    try:
        import pytesseract
        from pdf2image import convert_from_path
    except ImportError:
        console.print("[red]✗[/red] OCR 功能需要额外依赖:")
        console.print("  pip install docforge[ocr]")
        console.print("  以及系统依赖: sudo apt install tesseract-ocr poppler-utils")
        raise SystemExit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("正在转换 PDF 为图片...", total=None)

        try:
            images = convert_from_path(input_file, dpi=dpi)
        except Exception as e:
            console.print(f"[red]✗[/red] PDF 转图片失败: {e}")
            raise SystemExit(1)

        progress.update(task, description=f"正在 OCR 识别 ({len(images)} 页)...")

        all_text = []
        for i, image in enumerate(images, 1):
            try:
                text = pytesseract.image_to_string(image, lang=lang)
                if output_format == "markdown":
                    all_text.append(f"## 第 {i} 页\n\n{text.strip()}\n")
                else:
                    all_text.append(f"--- 第 {i} 页 ---\n{text.strip()}\n")
            except Exception as e:
                msg = f"[OCR 识别失败: {e}]"
                if output_format == "markdown":
                    all_text.append(f"## 第 {i} 页\n\n{msg}\n")
                else:
                    all_text.append(f"--- 第 {i} 页 ---\n{msg}\n")

    # Write output
    separator = "\n" if output_format == "markdown" else "\n"
    with open(output, "w", encoding="utf-8") as f:
        f.write(separator.join(all_text))

    console.print(f"[green]✓[/green] OCR 完成！共 {len(images)} 页，输出：{output}")
