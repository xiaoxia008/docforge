"""DocForge 核心功能测试"""

import os
import tempfile

import pytest
from fpdf import FPDF
from click.testing import CliRunner

from docforge.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def test_pdf():
    """创建测试 PDF 文件"""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Test Page 1", ln=True)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Test Page 2", ln=True)
        pdf.output(f.name)
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def test_pdf2():
    """创建第二个测试 PDF 文件"""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Second PDF", ln=True)
        pdf.output(f.name)
        yield f.name
    os.unlink(f.name)


class TestCLI:
    """测试 CLI 基本功能"""

    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "DocForge" in result.output

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_all_commands_registered(self, runner):
        result = runner.invoke(cli, ["--help"])
        commands = ["merge", "split", "compress", "extract", "watermark",
                     "encrypt", "decrypt", "to-images", "from-images", "ocr"]
        for cmd in commands:
            assert cmd in result.output, f"Command {cmd} not found"


class TestMerge:
    """测试 PDF 合并"""

    def test_merge_basic(self, runner, test_pdf, test_pdf2):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as out:
            result = runner.invoke(cli, ["merge", test_pdf, test_pdf2, "-o", out.name])
            assert result.exit_code == 0
            assert os.path.exists(out.name)
            assert os.path.getsize(out.name) > 0
            os.unlink(out.name)

    def test_merge_help(self, runner):
        result = runner.invoke(cli, ["merge", "--help"])
        assert result.exit_code == 0


class TestSplit:
    """测试 PDF 拆分"""

    def test_split_each(self, runner, test_pdf):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "page.pdf")
            result = runner.invoke(cli, ["split", test_pdf, "--each", "-o", output])
            assert result.exit_code == 0
            # Should create 2 files (2 pages)
            files = [f for f in os.listdir(tmpdir) if f.endswith(".pdf")]
            assert len(files) == 2

    def test_split_pages(self, runner, test_pdf):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as out:
            result = runner.invoke(cli, ["split", test_pdf, "--pages", "1", "-o", out.name])
            assert result.exit_code == 0
            assert os.path.exists(out.name)
            os.unlink(out.name)


class TestExtract:
    """测试文字提取"""

    def test_extract_text(self, runner, test_pdf):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as out:
            result = runner.invoke(cli, ["extract", test_pdf, "-o", out.name])
            assert result.exit_code == 0
            assert os.path.exists(out.name)
            with open(out.name, "r") as f:
                content = f.read()
            assert len(content) > 0
            os.unlink(out.name)


class TestWatermark:
    """测试水印功能"""

    def test_text_watermark(self, runner, test_pdf):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as out:
            result = runner.invoke(cli, ["watermark", test_pdf, "--text", "TEST", "-o", out.name])
            assert result.exit_code == 0
            assert os.path.exists(out.name)
            assert os.path.getsize(out.name) > 0
            os.unlink(out.name)


class TestEncrypt:
    """测试加密解密"""

    def test_encrypt_decrypt(self, runner, test_pdf):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as encrypted:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as decrypted:
                # Encrypt
                result = runner.invoke(cli, ["encrypt", test_pdf, "--password", "test123",
                                              "-o", encrypted.name])
                assert result.exit_code == 0
                assert os.path.exists(encrypted.name)

                # Decrypt
                result = runner.invoke(cli, ["decrypt", encrypted.name, "--password", "test123",
                                              "-o", decrypted.name])
                assert result.exit_code == 0
                assert os.path.exists(decrypted.name)

                os.unlink(encrypted.name)
                os.unlink(decrypted.name)


class TestCompress:
    """测试压缩功能"""

    def test_compress(self, runner, test_pdf):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as out:
            result = runner.invoke(cli, ["compress", test_pdf, "-o", out.name])
            assert result.exit_code == 0
            assert os.path.exists(out.name)
            assert os.path.getsize(out.name) > 0
            os.unlink(out.name)
