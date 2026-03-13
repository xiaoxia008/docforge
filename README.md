# DocForge 🔨

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![GitHub Stars](https://img.shields.io/github/stars/xiaoxia008/docforge)

**纯本地运行的 PDF/文档智能处理 CLI 工具 — 隐私安全，开箱即用**

## 安装

```bash
pip install -e .
```

如需 PDF 转图片功能，请额外安装依赖：

```bash
pip install pdf2image
# Linux 还需安装 poppler-utils
sudo apt install poppler-utils
```

## 使用说明

### 查看帮助

```bash
docforge --help
docforge merge --help
```

### 合并 PDF

```bash
docforge merge file1.pdf file2.pdf -o output.pdf
docforge merge *.pdf -o combined.pdf
```

### 拆分 PDF

```bash
# 按页码范围拆分
docforge split input.pdf --pages 1-5 -o output.pdf

# 指定多个页码
docforge split input.pdf --pages 1,3,5-8 -o output.pdf

# 每页单独拆分
docforge split input.pdf --each -o output_dir/
```

### 压缩 PDF

```bash
docforge compress input.pdf -o output.pdf --quality medium
```

支持 `low`、`medium`、`high` 三种压缩质量。

### 提取文字

```bash
# 提取为纯文本
docforge extract input.pdf -o output.txt

# 提取为 Markdown
docforge extract input.pdf --format markdown -o output.md
```

### 添加水印

```bash
# 文字水印
docforge watermark input.pdf --text "CONFIDENTIAL" -o output.pdf

# 图片水印
docforge watermark input.pdf --image logo.png -o output.pdf

# 设置透明度
docforge watermark input.pdf --text "DRAFT" --opacity 0.2 -o output.pdf
```

### 加密/解密

```bash
# 加密
docforge encrypt input.pdf -o output.pdf
# 会提示输入密码

# 解密
docforge decrypt input.pdf -o output.pdf
# 会提示输入密码
```

### PDF 转图片

```bash
docforge to-images input.pdf -o output_dir/ --format png --dpi 150
```

支持 `png`、`jpeg`、`webp` 格式。

### 图片转 PDF

```bash
docforge from-images img1.jpg img2.png -o output.pdf
docforge from-images *.jpg -o output.pdf
```

## 完整命令列表

| 命令 | 说明 |
|------|------|
| `merge` | 合并多个 PDF |
| `split` | 拆分 PDF |
| `compress` | 压缩 PDF |
| `extract` | 提取文字 |
| `watermark` | 添加水印 |
| `encrypt` | 加密 PDF |
| `decrypt` | 解密 PDF |
| `to-images` | PDF 转图片 |
| `from-images` | 图片转 PDF |

## 隐私声明

所有处理均在本地完成，不会上传任何文件到云端。

## License

MIT
