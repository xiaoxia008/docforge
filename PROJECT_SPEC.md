# DocForge - PDF/文档智能处理 CLI 工具

## 项目概述
一个纯本地运行的 PDF/文档处理命令行工具，主打隐私安全和易用性。

## 目标用户
办公人员、学生、法务/财务人员

## 技术栈
- Python 3.8+
- Click (CLI框架)
- pypdf (PDF处理)
- Pillow (图片处理)
- rich (终端美化输出)

## 核心功能 (MVP)

### 1. PDF 合并
```bash
docforge merge file1.pdf file2.pdf -o output.pdf
docforge merge *.pdf -o combined.pdf
```

### 2. PDF 拆分
```bash
docforge split input.pdf --pages 1-5 -o output.pdf
docforge split input.pdf --each -o output_dir/
```

### 3. PDF 压缩
```bash
docforge compress input.pdf -o output.pdf --quality medium
```

### 4. 提取文字
```bash
docforge extract input.pdf -o output.txt
docforge extract input.pdf --format markdown -o output.md
```

### 5. 加水印
```bash
docforge watermark input.pdf --text "CONFIDENTIAL" -o output.pdf
docforge watermark input.pdf --image logo.png -o output.pdf
```

### 6. PDF 加密/解密
```bash
docforge encrypt input.pdf --password xxx -o output.pdf
docforge decrypt input.pdf --password xxx -o output.pdf
```

### 7. PDF 转图片
```bash
docforge to-images input.pdf -o output_dir/ --format png
```

### 8. 图片转 PDF
```bash
docforge from-images *.jpg -o output.pdf
```

## 项目结构
```
docforge/
├── setup.py
├── requirements.txt
├── README.md
├── LICENSE (MIT)
├── docforge/
│   ├── __init__.py
│   ├── cli.py          # CLI 入口
│   ├── commands/
│   │   ├── merge.py
│   │   ├── split.py
│   │   ├── compress.py
│   │   ├── extract.py
│   │   ├── watermark.py
│   │   ├── encrypt.py
│   │   └── convert.py
│   └── utils.py
└── tests/
```

## 命名规范
- 命令用英文，简洁明了
- 输出信息用中文（目标用户是国内用户）
- 错误信息要友好，告诉用户怎么解决

## 非目标 (MVP不做)
- GUI 界面
- OCR (后续版本)
- 表格提取 (后续版本)
- 云端处理
