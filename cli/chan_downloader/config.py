"""Configuration management for chan-downloader."""

import json
import os
from pathlib import Path
from . import __version__

class Config:
    """Configuration manager."""
    
    DEFAULT_CONFIG = {
        "max_workers": 5,
        "default_theme": "light", 
        "default_sleep": 0,
        "skip_existing_threads": True,
        "create_index": True,
        "base_download_dir": "4chan_downloader",
        "media_subfolder": "media",
        "timeout": 300,
        "user_agent": f"chan-downloader/{__version__}",
    }
    
    def __init__(self, config_file="4chan_config.json"):
        self.config_file = Path(config_file)
        self._config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
            except Exception as e:
                from .utils import Console
                Console.print_warning(f"Error loading config: {e}. Using defaults.")
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            from .utils import Console
            Console.print_warning(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value."""
        self._config[key] = value
    
    def get_all(self):
        """Get all configuration values."""
        return self._config.copy()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self._config = self.DEFAULT_CONFIG.copy()
        self.save()
    
    def get_version(self):
        """Get version string."""
        return __version__
