"""PDF 加密/解密功能模块"""

import click
from pypdf import PdfReader, PdfWriter
from rich.console import Console

from docforge.utils import ensure_output_dir, handle_error, validate_pdf

console = Console()


@click.command("encrypt")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--password", "-p", required=True, prompt=True, hide_input=True, confirmation_prompt=True, help="加密密码")
@click.option("-o", "--output", default=None, help="输出文件路径")
def encrypt(input_file, password, output):
    """加密 PDF 文件。

    示例:
        docforge encrypt input.pdf --password xxx -o output.pdf
    """
    try:
        if not validate_pdf(input_file):
            raise SystemExit(1)

        if output is None:
            base, ext = input_file.rsplit(".", 1)
            output = f"{base}_encrypted.{ext}"

        ensure_output_dir(output)

        reader = PdfReader(input_file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        with open(output, "wb") as f:
            writer.write(f)

        console.print(f"[green]✓ 加密成功！输出：{output}[/green]")

    except Exception as e:
        handle_error(e, "PDF 加密失败")


@click.command("decrypt")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--password", "-p", required=True, prompt=True, hide_input=True, help="解密密码")
@click.option("-o", "--output", default=None, help="输出文件路径")
def decrypt(input_file, password, output):
    """解密 PDF 文件。

    示例:
        docforge decrypt input.pdf --password xxx -o output.pdf
    """
    try:
        if not validate_pdf(input_file):
            raise SystemExit(1)

        if output is None:
            base, ext = input_file.rsplit(".", 1)
            output = f"{base}_decrypted.{ext}"

        ensure_output_dir(output)

        reader = PdfReader(input_file)

        if reader.is_encrypted:
            result = reader.decrypt(password)
            if result == 0:
                console.print("[red]错误：密码不正确，无法解密文件[/red]")
                raise SystemExit(1)

        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        with open(output, "wb") as f:
            writer.write(f)

        console.print(f"[green]✓ 解密成功！输出：{output}[/green]")

    except SystemExit:
        raise
    except Exception as e:
        handle_error(e, "PDF 解密失败")
