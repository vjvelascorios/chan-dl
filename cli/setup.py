from setuptools import setup, find_packages
import os

# Leer el README para la descripción larga
def read_long_description():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    return "Advanced 4chan thread and board downloader with modern HTML interface"

setup(
    name="chan-downloader",
    version="16.2.0",
    author="vjvelascorios",
    author_email="your.email@example.com",
    description="Advanced 4chan thread and board downloader with modern HTML interface",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chan-downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "basc-py4chan>=2.0.4",
        "gallery-dl>=1.25.0",
        "tqdm>=4.64.0",
        "pathlib2>=2.3.7; python_version<'3.4'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ]
    },
    entry_points={
        "console_scripts": [
            "chan-dl=chan_downloader.cli:main",
            "4chan-dl=chan_downloader.cli:main",
            "chandownloader=chan_downloader.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/chan-downloader/issues",
        "Documentation": "https://github.com/yourusername/chan-downloader/blob/main/README.md",
        "Source": "https://github.com/yourusername/chan-downloader",
    },
    keywords="4chan downloader imageboard scraper html offline archive",
    include_package_data=True,
    zip_safe=False,
)
