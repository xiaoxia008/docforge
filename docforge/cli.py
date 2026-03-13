"""DocForge CLI 入口模块"""

import click
from rich.console import Console

from docforge import __version__
from docforge.commands.compress import compress
from docforge.commands.convert import from_images, to_images
from docforge.commands.encrypt import decrypt, encrypt
from docforge.commands.extract import extract
from docforge.commands.merge import merge
from docforge.commands.split import split
from docforge.commands.watermark import watermark

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="DocForge")
def cli():
    """DocForge - PDF/文档智能处理 CLI 工具

    一个纯本地运行的 PDF/文档处理命令行工具，主打隐私安全和易用性。
    """
    pass


cli.add_command(merge)
cli.add_command(split)
cli.add_command(compress)
cli.add_command(extract)
cli.add_command(watermark)
cli.add_command(encrypt)
cli.add_command(decrypt)
cli.add_command(to_images)
cli.add_command(from_images)


if __name__ == "__main__":
    cli()
