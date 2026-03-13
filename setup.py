"""DocForge 安装配置"""

from setuptools import find_packages, setup

setup(
    name="docforge",
    version="0.1.0",
    description="PDF/文档智能处理 CLI 工具",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="DocForge Team",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0",
        "pypdf>=3.0",
        "Pillow>=9.0",
        "rich>=12.0",
        "reportlab>=4.0",
    ],
    extras_require={
        "images": ["pdf2image>=1.16"],
    },
    entry_points={
        "console_scripts": [
            "docforge=docforge.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
    ],
)
