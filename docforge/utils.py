"""DocForge 工具函数模块"""

import os
import sys

from rich.console import Console

console = Console()


def validate_pdf(file_path: str) -> bool:
    """验证文件是否为有效的 PDF 文件。

    Args:
        file_path: 文件路径。

    Returns:
        如果文件是有效的 PDF 则返回 True，否则返回 False。
    """
    if not os.path.exists(file_path):
        console.print(f"[red]错误：文件不存在 - {file_path}[/red]")
        return False
    if not file_path.lower().endswith(".pdf"):
        console.print(f"[red]错误：不是 PDF 文件 - {file_path}[/red]")
        return False
    return True


def ensure_output_dir(output_path: str) -> None:
    """确保输出目录存在。

    Args:
        output_path: 输出文件路径或目录路径。
    """
    dir_path = os.path.dirname(output_path) if "." in os.path.basename(output_path) else output_path
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def get_file_size_str(file_path: str) -> str:
    """获取文件大小的可读字符串。

    Args:
        file_path: 文件路径。

    Returns:
        格式化的文件大小字符串。
    """
    size = os.path.getsize(file_path)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def handle_error(e: Exception, context: str = "") -> None:
    """统一错误处理。

    Args:
        e: 异常对象。
        context: 错误上下文描述。
    """
    msg = f"错误：{context} - {e}" if context else f"错误：{e}"
    console.print(f"[red]{msg}[/red]")
    sys.exit(1)
