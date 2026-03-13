"""PDF 与图片互转功能模块"""

import os

import click
from rich.console import Console
from rich.progress import track

from docforge.utils import ensure_output_dir, get_file_size_str, handle_error

console = Console()


@click.command("to-images")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", default="images", help="输出目录")
@click.option(
    "--format",
    "img_format",
    type=click.Choice(["png", "jpeg", "webp"]),
    default="png",
    help="输出图片格式",
    show_default=True,
)
@click.option("--dpi", default=150, type=int, help="输出图片 DPI", show_default=True)
def to_images(input_file, output, img_format, dpi):
    """将 PDF 每一页转换为图片。

    示例:
        docforge to-images input.pdf -o output_dir/ --format png
    """
    try:
        if not input_file.lower().endswith(".pdf"):
            console.print("[red]错误：输入文件不是 PDF 格式[/red]")
            raise SystemExit(1)

        ensure_output_dir(output)
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        try:
            from pdf2image import convert_from_path

            images = convert_from_path(input_file, dpi=dpi)
        except ImportError:
            console.print("[red]错误：pdf2image 未安装，请运行: pip install pdf2image[/red]")
            console.print("[yellow]提示：还需要安装 poppler-utils (Linux: apt install poppler-utils)[/yellow]")
            raise SystemExit(1)

        saved_files = []
        for i, img in enumerate(track(images, description="[cyan]正在转换...[/cyan]"), 1):
            out_path = os.path.join(output, f"{base_name}_page_{i}.{img_format}")
            img.save(out_path, img_format.upper())
            saved_files.append(out_path)

        console.print(
            f"[green]✓ 转换成功！共 {len(saved_files)} 页图片，输出目录：{output}[/green]"
        )

    except SystemExit:
        raise
    except Exception as e:
        handle_error(e, "PDF 转图片失败")


@click.command("from-images")
@click.argument("images", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("-o", "--output", default="output.pdf", help="输出 PDF 文件路径", show_default=True)
def from_images(images, output):
    """将多张图片合并为一个 PDF 文件。

    示例:
        docforge from-images *.jpg -o output.pdf
    """
    try:
        from PIL import Image

        ensure_output_dir(output)

        img_list = []
        for img_path in track(images, description="[cyan]正在处理图片...[/cyan]"):
            img = Image.open(img_path)
            if img.mode == "RGBA":
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            img_list.append(img)

        if not img_list:
            console.print("[red]错误：没有有效的图片文件[/red]")
            raise SystemExit(1)

        img_list[0].save(output, "PDF", save_all=True, append_images=img_list[1:])

        size_str = get_file_size_str(output)
        console.print(
            f"[green]✓ 转换成功！共 {len(img_list)} 张图片，输出：{output} ({size_str})[/green]"
        )

    except SystemExit:
        raise
    except Exception as e:
        handle_error(e, "图片转 PDF 失败")
