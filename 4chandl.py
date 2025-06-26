# v16.2 - Mejoras múltiples
import basc_py4chan
import os
import sys
import re
import argparse
import subprocess
import shutil
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from pathlib import Path

# --- Constantes y Configuración Global ---
BASE_DOWNLOAD_DIR = "4chan_downloader"
MEDIA_SUBFOLDER = "media"
MAX_WORKERS = 5
CONFIG_FILE = "4chan_config.json"

class Console:
    """Clase para imprimir mensajes con colores en la consola."""
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BLUE = '\033[94m'
    
    @staticmethod
    def print_success(message): print(f"{Console.OKGREEN}{message}{Console.ENDC}")
    @staticmethod
    def print_warning(message): print(f"{Console.WARNING}{message}{Console.ENDC}")
    @staticmethod
    def print_error(message): print(f"{Console.FAIL}{message}{Console.ENDC}", file=sys.stderr)
    @staticmethod
    def print_info(message): print(message)
    @staticmethod
    def print_header(message): print(f"{Console.BLUE}{message}{Console.ENDC}")

def load_config():
    """Carga configuración desde archivo JSON."""
    default_config = {
        "max_workers": 5,
        "default_theme": "light",
        "default_sleep": 0,
        "skip_existing_threads": True,
        "create_index": True
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return {**default_config, **config}
        except Exception as e:
            Console.print_warning(f"Error cargando config: {e}. Usando valores por defecto.")
    
    return default_config

def save_config(config):
    """Guarda configuración en archivo JSON."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        Console.print_warning(f"Error guardando config: {e}")

def check_dependencies():
    """Verifica si las dependencias externas están instaladas."""
    dependencies = ["gallery-dl"]
    missing = []
    
    for dep in dependencies:
        if not shutil.which(dep):
            missing.append(dep)
    
    if missing:
        Console.print_error(f"[ERROR CRÍTICO] Dependencias faltantes: {', '.join(missing)}")
        Console.print_error("Instala con: pip install gallery-dl")
        sys.exit(1)
    
    Console.print_success("Todas las dependencias están instaladas.")

def sanitize_filename(name):
    """Limpia un string para que sea un nombre de archivo/carpeta válido."""
    if not name or name.isspace():
        return "Sin_Nombre"
    
    sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
    sanitized_name = sanitized_name.replace(" ", "_").strip("._-")
    return sanitized_name[:100] if sanitized_name else "Sin_Nombre"

def format_file_size(size_bytes):
    """Convierte bytes a formato legible."""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def get_media_info(media_folder):
    """Obtiene información detallada de los archivos de media."""
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

def calculate_reading_time(thread):
    """Calcula el tiempo estimado de lectura basado en el contenido del hilo."""
    total_words = 0
    
    for post in thread.all_posts:
        if post.comment:
            # Remover HTML tags y contar palabras
            clean_text = re.sub(r'<[^>]+>', '', post.comment)
            # Remover caracteres especiales y saltos de línea
            clean_text = re.sub(r'[^\w\s]', ' ', clean_text)
            words = len(clean_text.split())
            total_words += words
    
    # Promedio de palabras por minuto (200-250 es típico para lectura casual)
    words_per_minute = 220
    reading_time_minutes = total_words / words_per_minute
    
    # Formatear tiempo
    if reading_time_minutes < 1:
        return "< 1 min"
    elif reading_time_minutes < 60:
        return f"{reading_time_minutes:.0f} min"
    else:
        hours = reading_time_minutes // 60
        minutes = reading_time_minutes % 60
        if minutes < 30:
            return f"{hours:.0f}h"
        else:
            return f"{hours:.0f}h {minutes:.0f}m"

def create_thread_html(thread, board_name, thread_id, thread_subject, downloaded_files, initial_theme='light'):
    """Genera HTML mejorado con mejor información y estilos."""
    media_info = get_media_info(os.path.join(BASE_DOWNLOAD_DIR, board_name, f"{thread_id}_{sanitize_filename(thread_subject)}", MEDIA_SUBFOLDER))
    reading_time = calculate_reading_time(thread)
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>/{board_name}/ - {thread_subject} ({thread_id})</title>
    <style>
        :root {{
            --primary-color: #0d86ff;
            --success-color: #28a745;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
        }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 1em; line-height: 1.6; transition: all 0.3s ease; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 1em; }}
        .thread-info {{ background: rgba(255,255,255,0.1); padding: 1em; border-radius: 8px; margin-bottom: 1em; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1em; font-size: 0.9em; }}
        .stat {{ background: rgba(0,0,0,0.1); padding: 0.8em; border-radius: 6px; text-align: center; transition: transform 0.2s; }}
        .stat:hover {{ transform: translateY(-2px); }}
        .stat-value {{ font-size: 1.2em; font-weight: bold; display: block; }}
        .stat-label {{ font-size: 0.85em; opacity: 0.8; margin-top: 0.2em; }}
        a {{ text-decoration: none; color: var(--primary-color); }} a:hover {{ text-decoration: underline; }}
        img, video {{ max-width: 100%; max-height: 500px; height: auto; cursor: pointer; border-radius: 6px; margin: 0.5em 0; }}
        .media-container {{ text-align: center; margin: 1em 0; }}
        .post {{ margin-bottom: 1.5em; padding: 1.2em; border-radius: 10px; transition: all 0.3s; border: 1px solid transparent; }}
        .post:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .post-header {{ font-size: 0.9em; margin-bottom: 0.8em; display: flex; justify-content: space-between; align-items: center; }}
        .post-id {{ font-weight: bold; }}
        .post-comment {{ word-wrap: break-word; font-size: 1em; line-height: 1.6; }}
        .theme-toggle {{ position: fixed; top: 20px; right: 20px; padding: 10px 15px; border-radius: 25px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.2); transition: all 0.3s; z-index: 1000; }}
        .theme-toggle:hover {{ transform: scale(1.05); }}
        footer {{ text-align: center; margin-top: 3em; padding: 2em 0; border-top: 2px solid; font-size: 0.85em; opacity: 0.7; }}
        
        /* Temas */
        body.light-theme {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); color: #2c3e50; }}
        .light-theme .post {{ background: rgba(255,255,255,0.9); border-color: #e1e8ed; }}
        .light-theme .post-id {{ color: #e74c3c; }}
        .light-theme .theme-toggle {{ background: #34495e; color: white; }}
        .light-theme footer {{ border-color: #bdc3c7; }}
        
        body.dark-theme {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ecf0f1; }}
        .dark-theme .post {{ background: rgba(44,62,80,0.9); border-color: #34495e; }}
        .dark-theme .post-id {{ color: #e67e22; }}
        .dark-theme .theme-toggle {{ background: #ecf0f1; color: #2c3e50; }}
        .dark-theme footer {{ border-color: #34495e; }}
        
        .quote {{ color: #27ae60; font-style: italic; }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 0.5em; }}
            .stats {{ grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 0.8em; }}
            .stat {{ padding: 0.6em; }}
            img, video {{ max-height: 300px; }}
        }}
    </style>
</head>
<body class="{initial_theme}-theme">
    <button id="theme-toggle" class="theme-toggle">🌙</button>
    <div class="container">
        <div class="thread-info">
            <h1><a href="{thread.url}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
            <div class="stats">
                <div class="stat">
                    <span class="stat-value">📝 {len(thread.all_posts)}</span>
                    <div class="stat-label">Posts</div>
                </div>
                <div class="stat">
                    <span class="stat-value">🖼️ {media_info['count']}</span>
                    <div class="stat-label">Archivos</div>
                </div>
                <div class="stat">
                    <span class="stat-value">💾 {media_info['formatted_total_size']}</span>
                    <div class="stat-label">Tamaño</div>
                </div>
                <div class="stat">
                    <span class="stat-value">📖 {reading_time}</span>
                    <div class="stat-label">Lectura</div>
                </div>
                <div class="stat">
                    <span class="stat-value">🕒 {datetime.now().strftime('%H:%M')}</span>
                    <div class="stat-label">Descargado</div>
                </div>
            </div>
        </div>
    """
    
    # Crear un conjunto para rastrear archivos ya utilizados
    used_files = set()
    available_files = list(downloaded_files)
    
    for post in thread.all_posts:
        html_content += f"""
        <div class="post">
            <div class="post-header">
                <span class="post-id">#{post.post_id}</span>
                <span>{post.datetime.strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
            <div class="post-comment">
        """
        
        if post.has_file and post.file:
            actual_filename = None
            remaining_files = [f for f in available_files if f not in used_files]
            
            # Improved file matching logic
            for downloaded_file in remaining_files:
                if (post.file.filename in downloaded_file and 
                    post.file.file_extension.lower() in downloaded_file.lower()):
                    actual_filename = downloaded_file
                    break
            
            if not actual_filename:
                for downloaded_file in remaining_files:
                    if os.path.splitext(downloaded_file)[1].lower() == post.file.file_extension.lower():
                        actual_filename = downloaded_file
                        break
            
            if actual_filename:
                used_files.add(actual_filename)
                file_path_relative = f"{MEDIA_SUBFOLDER}/{actual_filename}"
                file_extension = os.path.splitext(actual_filename)[1].lower()
                
                html_content += '<div class="media-container">'
                if file_extension in ['.webm', '.mp4', '.mov']:
                    html_content += f'<video controls muted loop preload="metadata"><source src="{file_path_relative}" type="video/{file_extension[1:]}"></video>'
                else:
                    html_content += f'<a href="{file_path_relative}" target="_blank"><img src="{file_path_relative}" alt="{actual_filename}" loading="lazy"></a>'
                html_content += '</div>'
        
        html_content += f"{post.comment}</div></div>"
    
    html_content += f"""
        <footer>
            <p>Generado por 4chan Downloader v16.2 - <a href="https://github.com" target="_blank">GitHub</a></p>
            <p>Descargado el {datetime.now().strftime('%Y-%m-%d a las %H:%M:%S')}</p>
        </footer>
    </div>
    <script>
        const toggle = document.getElementById('theme-toggle');
        const body = document.body;
        
        function setTheme(theme) {{
            body.className = theme + '-theme';
            toggle.textContent = theme === 'light' ? '🌙' : '☀️';
            localStorage.setItem('4chan-theme', theme);
        }}
        
        toggle.addEventListener('click', () => {{
            const current = body.classList.contains('light-theme') ? 'light' : 'dark';
            setTheme(current === 'light' ? 'dark' : 'light');
        }});
        
        // Load saved theme
        const saved = localStorage.getItem('4chan-theme') || '{initial_theme}';
        setTheme(saved);
        
        // Add image click to expand
        document.querySelectorAll('img').forEach(img => {{
            img.addEventListener('click', () => {{
                if (img.style.maxWidth === 'none') {{
                    img.style.maxWidth = '100%';
                    img.style.maxHeight = '500px';
                }} else {{
                    img.style.maxWidth = 'none';
                    img.style.maxHeight = 'none';
                }}
            }});
        }});
    </script>
</body></html>"""
    
    return html_content

def create_board_index(board_name, results, config):
    """Crea un índice HTML para el board completo."""
    if not config.get("create_index", True):
        return
    
    successful_threads = [r for r in results if r is not None]
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice del Board /{board_name}/</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 2em; background: #f8f9fa; }}
        .header {{ text-align: center; margin-bottom: 2em; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1em; margin-bottom: 2em; }}
        .stat-card {{ background: white; padding: 1.5em; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .threads {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1em; }}
        .thread-card {{ background: white; padding: 1em; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; }}
        .thread-card:hover {{ transform: translateY(-4px); }}
        .thread-title {{ font-weight: bold; margin-bottom: 0.5em; }}
        .thread-id {{ color: #666; font-size: 0.9em; }}
        a {{ text-decoration: none; color: inherit; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Board /{board_name}/</h1>
        <p>Descargado el {datetime.now().strftime('%Y-%m-%d a las %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>{len(successful_threads)}</h3>
            <p>Hilos Descargados</p>
        </div>
        <div class="stat-card">
            <h3>{len(results) - len(successful_threads)}</h3>
            <p>Hilos Fallidos</p>
        </div>
    </div>
    
    <div class="threads">
    """
    
    for thread_data in successful_threads:
        thread_id = thread_data["id"]
        subject = thread_data["subject"]
        sanitized_subject = sanitize_filename(subject)
        folder_name = f"{thread_id}_{sanitized_subject}"
        html_file = f"{thread_id}_{sanitized_subject}.html"
        
        html_content += f"""
        <div class="thread-card">
            <a href="{folder_name}/{html_file}">
                <div class="thread-title">{subject}</div>
                <div class="thread-id">ID: {thread_id}</div>
            </a>
        </div>
        """
    
    html_content += """
    </div>
</body></html>
    """
    
    index_path = os.path.join(BASE_DOWNLOAD_DIR, board_name, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    Console.print_success(f"Índice del board creado: {index_path}")

def download_thread(board_name, thread_id, theme='light', overwrite=False, sleep_time=0, config=None):
    """Función mejorada de descarga de hilos."""
    if config is None:
        config = load_config()
    
    try:
        # Check if thread already exists and skip if configured
        thread_folder = os.path.join(BASE_DOWNLOAD_DIR, board_name, f"{thread_id}_*")
        existing = list(Path(BASE_DOWNLOAD_DIR).glob(f"{board_name}/{thread_id}_*"))
        
        if existing and config.get("skip_existing_threads", True) and not overwrite:
            Console.print_info(f"    > Hilo {thread_id} ya existe, saltando...")
            return {"id": thread_id, "subject": "Existente"}
        
        board = basc_py4chan.Board(board_name)
        thread = board.get_thread(thread_id)
        if not thread:
            Console.print_warning(f"El hilo {thread_id} en /{board_name}/ ya no existe.")
            return None
        
        thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
        sanitized_subject = sanitize_filename(thread_subject)
        
        folder_name = f"{thread_id}_{sanitized_subject}"
        thread_folder = os.path.join(BASE_DOWNLOAD_DIR, board_name, folder_name)
        media_folder = os.path.join(thread_folder, MEDIA_SUBFOLDER)
        os.makedirs(media_folder, exist_ok=True)
        
        Console.print_info(f"    > Procesando: {thread_subject[:50]}...")
        
        # Enhanced gallery-dl command
        command = [
            'gallery-dl',
            '--directory', media_folder,
            '-o', 'path=.',
            '-o', 'filename={filename}.{extension}',
            '--write-info-json'  # Save metadata
        ]
        
        if sleep_time > 0:
            command.extend(['--sleep', str(sleep_time)])
        
        if overwrite:
            command.append('--no-skip')
        
        command.append(thread.url)
        
        # Execute with timeout
        try:
            process = subprocess.run(command, capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            Console.print_warning(f"    > Timeout en descarga del hilo {thread_id}")
            return None
        
        # Get media info
        media_info = get_media_info(media_folder)
        Console.print_success(f"    > Descargados {media_info['count']} archivos ({media_info['formatted_total_size']})")
        
        # Generate HTML
        downloaded_files = set(os.listdir(media_folder)) if os.path.exists(media_folder) else set()
        html_content = create_thread_html(thread, board_name, thread_id, thread_subject, downloaded_files, theme)
        
        html_filename = f"{thread_id}_{sanitized_subject}.html"
        html_path = os.path.join(thread_folder, html_filename)
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return {"id": thread_id, "subject": thread_subject}
        
    except Exception as e:
        Console.print_error(f"Error procesando hilo {thread_id}: {str(e)}")
        return None

def download_board(board_name, theme='light', overwrite=False, multithread=False, sleep_time=0):
    """Función mejorada de descarga de boards."""
    config = load_config()
    
    try:
        board = basc_py4chan.Board(board_name)
        all_thread_ids = board.get_all_thread_ids()
        Console.print_header(f"📋 Procesando /{board_name}/ - {len(all_thread_ids)} hilos encontrados")
    except Exception as e:
        Console.print_error(f"Error obteniendo hilos de /{board_name}/: {e}")
        return
    
    start_time = time.time()
    results = []
    
    if multithread:
        max_workers = config.get("max_workers", MAX_WORKERS)
        Console.print_info(f"🚀 Modo multi-hilo activado ({max_workers} workers)")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            args = [(board_name, tid, theme, overwrite, sleep_time, config) for tid in all_thread_ids]
            results = list(tqdm(
                executor.map(lambda p: download_thread(*p), args),
                total=len(all_thread_ids),
                desc="Descargando hilos"
            ))
    else:
        Console.print_info("⏳ Modo secuencial activado")
        for thread_id in tqdm(all_thread_ids, desc="Descargando hilos"):
            results.append(download_thread(board_name, thread_id, theme, overwrite, sleep_time, config))
    
    # Statistics
    elapsed = time.time() - start_time
    success_count = sum(1 for r in results if r is not None)
    
    Console.print_header("\n📊 RESUMEN FINAL")
    Console.print_success(f"✅ Hilos exitosos: {success_count}/{len(all_thread_ids)}")
    Console.print_info(f"⏱️  Tiempo total: {elapsed:.1f} segundos")
    Console.print_info(f"⚡ Promedio: {elapsed/len(all_thread_ids):.1f}s por hilo")
    
    # Create board index
    create_board_index(board_name, results, config)

def main():
    """Función principal mejorada."""
    config = load_config()
    
    parser = argparse.ArgumentParser(
        description="4chan Downloader v16.2 - Descargador avanzado con mejoras de rendimiento",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s "https://boards.4chan.org/g/thread/12345"
  %(prog)s "https://boards.4chan.org/g/" -mt -s 1.5
  %(prog)s "URL" --config-set max_workers 10
        """)
    
    parser.add_argument("url", help="URL del hilo o board de 4chan")
    parser.add_argument("-t", "--tema", choices=['light', 'dark'], 
                       default=config.get("default_theme", "light"),
                       help="Tema del HTML generado")
    parser.add_argument("--overwrite", action="store_true", 
                       help="Sobrescribir archivos existentes")
    parser.add_argument("-mt", "--multithread", action="store_true",
                       help="Activar procesamiento paralelo")
    parser.add_argument("-s", "--sleep", type=float, 
                       default=config.get("default_sleep", 0),
                       help="Delay entre descargas (segundos)")
    parser.add_argument("--config-set", nargs=2, metavar=("KEY", "VALUE"),
                       help="Establecer valor de configuración")
    parser.add_argument("--config-show", action="store_true",
                       help="Mostrar configuración actual")
    
    args = parser.parse_args()
    
    # Handle config operations
    if args.config_show:
        Console.print_info("Configuración actual:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        return
    
    if args.config_set:
        key, value = args.config_set
        try:
            # Try to convert to appropriate type
            if value.lower() in ['true', 'false']:
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            elif '.' in value and value.replace('.', '').isdigit():
                value = float(value)
        except:
            pass
        
        config[key] = value
        save_config(config)
        Console.print_success(f"Configuración actualizada: {key} = {value}")
        return
    
    # Main execution
    check_dependencies()
    Console.print_header("🚀 4chan Downloader v16.2 Iniciado")
    
    if args.sleep > 0:
        Console.print_info(f"⏱️  Delay configurado: {args.sleep}s entre descargas")
    
    # URL parsing
    board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
    thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)
    
    if thread_match:
        board_name, thread_id = thread_match.groups()
        result = download_thread(board_name, int(thread_id), args.tema, args.overwrite, args.sleep)
        if result:
            Console.print_success("✅ Hilo descargado exitosamente")
    elif board_match:
        board_name = board_match.group(1)
        download_board(board_name, args.tema, args.overwrite, args.multithread, args.sleep)
    else:
        Console.print_error("❌ URL no válida. Debe ser una URL de 4chan.")
        sys.exit(1)

if __name__ == "__main__":
    main()