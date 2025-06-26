"""
4chan Downloader - Advanced thread and board downloader with modern HTML interface.

A powerful tool for downloading and archiving 4chan threads and entire boards
with a beautiful, responsive HTML interface.
"""

__version__ = "16.2.0"
__author__ = "vjvelascorios"
__email__ = "vj.velascorios@gmail.com"
__license__ = "MIT"
__title__ = "chan-downloader"
__description__ = "Advanced 4chan thread and board downloader with modern HTML interface"

from .core import ChanDownloader
from .config import Config
from .utils import Console, format_file_size, sanitize_filename

__all__ = [
    "ChanDownloader",
    "Config", 
    "Console",
    "format_file_size",
    "sanitize_filename"
]
