"""Utility functions and classes."""

import os
import re
import sys

class Console:
    """Console output with colors."""
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BLUE = '\033[94m'
    
    @staticmethod
    def print_success(message): 
        print(f"{Console.OKGREEN}{message}{Console.ENDC}")
    
    @staticmethod
    def print_warning(message): 
        print(f"{Console.WARNING}{message}{Console.ENDC}")
    
    @staticmethod
    def print_error(message): 
        print(f"{Console.FAIL}{message}{Console.ENDC}", file=sys.stderr)
    
    @staticmethod
    def print_info(message): 
        print(message)
    
    @staticmethod
    def print_header(message): 
        print(f"{Console.BLUE}{message}{Console.ENDC}")

def sanitize_filename(name):
    """Clean string for valid filename."""
    if not name or name.isspace():
        return "Sin_Nombre"
    
    sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
    sanitized_name = sanitized_name.replace(" ", "_").strip("._-")
    return sanitized_name[:100] if sanitized_name else "Sin_Nombre"

def format_file_size(size_bytes):
    """Convert bytes to human readable format."""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def get_media_info(media_folder):
    """Get detailed information about media files."""
    if not os.path.exists(media_folder):
        return {"count": 0, "total_size": 0, "files": []}
    
    files_info = []
    total_size = 0
    
    for filename in os.listdir(media_folder):
        filepath = os.path.join(media_folder, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            total_size += size
            files_info.append({
                "name": filename,
                "size": size,
                "formatted_size": format_file_size(size)
            })
    
    return {
        "count": len(files_info),
        "total_size": total_size,
        "formatted_total_size": format_file_size(total_size),
        "files": files_info
    }
