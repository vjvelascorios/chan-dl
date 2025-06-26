"""Command line interface for chan-downloader."""

import argparse
import sys
import re
from .core import ChanDownloader
from .config import Config
from .utils import Console

def create_parser():
    """Create command line argument parser."""
    config = Config()
    
    parser = argparse.ArgumentParser(
        prog="chan-dl",
        description="4chan Downloader v16.2 - Advanced thread and board downloader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  chan-dl "https://boards.4chan.org/g/thread/12345"
  chan-dl "https://boards.4chan.org/g/" -mt -s 1.5
  chan-dl --config-set max_workers 10
  chan-dl --version
        """)
    
    parser.add_argument("url", nargs='?', help="URL of 4chan thread or board")
    parser.add_argument("-v", "--version", action="version", 
                       version=f"%(prog)s {config.get_version()}")
    parser.add_argument("-t", "--theme", choices=['light', 'dark'], 
                       default=config.get("default_theme", "light"),
                       help="HTML theme (default: %(default)s)")
    parser.add_argument("--overwrite", action="store_true", 
                       help="Overwrite existing files")
    parser.add_argument("-mt", "--multithread", action="store_true",
                       help="Enable parallel processing")
    parser.add_argument("-s", "--sleep", type=float, 
                       default=config.get("default_sleep", 0),
                       help="Delay between downloads in seconds (default: %(default)s)")
    parser.add_argument("-w", "--workers", type=int,
                       help="Number of parallel workers (overrides config)")
    parser.add_argument("--config-set", nargs=2, metavar=("KEY", "VALUE"),
                       help="Set configuration value")
    parser.add_argument("--config-show", action="store_true",
                       help="Show current configuration")
    parser.add_argument("--config-reset", action="store_true",
                       help="Reset configuration to defaults")
    parser.add_argument("-q", "--quiet", action="store_true",
                       help="Suppress non-error output")
    parser.add_argument("--output-dir", type=str,
                       help="Custom output directory")
    
    return parser

def validate_url(url):
    """Validate 4chan URL and extract components."""
    if not url:
        return None, None, None
        
    board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", url)
    thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", url)
    
    if thread_match:
        return "thread", thread_match.group(1), int(thread_match.group(2))
    elif board_match:
        return "board", board_match.group(1), None
    else:
        return None, None, None

def handle_config_operations(args, config):
    """Handle configuration-related operations."""
    if args.config_show:
        Console.print_info("Current configuration:")
        for key, value in config.get_all().items():
            print(f"  {key}: {value}")
        return True
    
    if args.config_reset:
        config.reset_to_defaults()
        Console.print_success("Configuration reset to defaults")
        return True
    
    if args.config_set:
        key, value = args.config_set
        try:
            # Auto-convert types
            if value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            elif '.' in value and value.replace('.', '').replace('-', '').isdigit():
                value = float(value)
        except (ValueError, AttributeError):
            pass
        
        config.set(key, value)
        config.save()
        Console.print_success(f"Configuration updated: {key} = {value}")
        return True
    
    return False

def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize configuration
    config = Config()
    if args.output_dir:
        config.set("base_download_dir", args.output_dir)
    
    # Handle config operations first
    if handle_config_operations(args, config):
        return 0
    
    # Require URL for download operations
    if not args.url:
        parser.print_help()
        Console.print_error("Error: URL is required for download operations")
        return 1
    
    # Validate URL
    url_type, board_name, thread_id = validate_url(args.url)
    if not url_type:
        Console.print_error("Invalid URL. Must be a 4chan thread or board URL.")
        return 1
    
    # Override config with command line args
    if args.workers:
        config.set("max_workers", args.workers)
    
    # Initialize downloader
    try:
        downloader = ChanDownloader(config, quiet=args.quiet)
        
        Console.print_header("🚀 4chan Downloader v16.2 Started")
        
        if args.sleep > 0:
            Console.print_info(f"⏱️  Delay configured: {args.sleep}s between downloads")
        
        # Execute download
        if url_type == "thread":
            result = downloader.download_thread(
                board_name, thread_id, 
                theme=args.theme, 
                overwrite=args.overwrite, 
                sleep_time=args.sleep
            )
            if result:
                Console.print_success("✅ Thread downloaded successfully")
                return 0
            else:
                Console.print_error("❌ Thread download failed")
                return 1
                
        elif url_type == "board":
            success = downloader.download_board(
                board_name,
                theme=args.theme,
                overwrite=args.overwrite,
                multithread=args.multithread,
                sleep_time=args.sleep
            )
            return 0 if success else 1
            
    except KeyboardInterrupt:
        Console.print_warning("\n⏹️  Download interrupted by user")
        return 130
    except Exception as e:
        Console.print_error(f"❌ Unexpected error: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
