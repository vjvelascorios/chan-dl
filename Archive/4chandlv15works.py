# # v15
# import basc_py4chan
# import os
# import sys
# import re
# import argparse
# import subprocess
# import shutil
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor
# from tqdm import tqdm

# # --- Constantes y Configuración Global ---
# BASE_DOWNLOAD_DIR = "4chan_downloader"
# MEDIA_SUBFOLDER = "media"  # Nombre de la subcarpeta para imágenes y videos
# MAX_WORKERS = 5

# class Console:
#     """Clase para imprimir mensajes con colores en la consola."""
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
    
#     @staticmethod
#     def print_success(message): print(f"{Console.OKGREEN}{message}{Console.ENDC}")
#     @staticmethod
#     def print_warning(message): print(f"{Console.WARNING}{message}{Console.ENDC}")
#     @staticmethod
#     def print_error(message): print(f"{Console.FAIL}{message}{Console.ENDC}", file=sys.stderr)
#     @staticmethod
#     def print_info(message): print(message)

# def check_dependencies():
#     """Verifica si las dependencias externas (gallery-dl) están instaladas."""
#     if not shutil.which("gallery-dl"):
#         Console.print_error("[ERROR CRÍTICO] El comando 'gallery-dl' no fue encontrado.")
#         Console.print_error("Por favor, asegúrate de que gallery-dl esté instalado: pip install gallery-dl")
#         sys.exit(1)
#     Console.print_success("Dependencia 'gallery-dl' encontrada.")

# def sanitize_filename(name):
#     """Limpia un string para que sea un nombre de archivo/carpeta válido."""
#     sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
#     sanitized_name = sanitized_name.replace(" ", "_")
#     return sanitized_name[:100]

# def create_thread_html(thread, board_name, thread_id, thread_subject, downloaded_files, initial_theme='light'):
#     """
#     Genera el HTML usando basc-py4chan para el texto y una lista de archivos verificados en disco.
#     Las rutas ahora apuntan a la subcarpeta MEDIA_SUBFOLDER.
#     """
#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="es">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>{board_name} - {thread_subject} ({thread_id})</title>
#         <style>
#             body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 1em; line-height: 1.6; transition: background-color 0.3s, color 0.3s; }}
#             .container {{ max-width: 800px; margin: 0 auto; padding: 1em; }}
#             a {{ text-decoration: none; }} a:hover {{ text-decoration: underline; }}
#             img, video {{ max-width: 350px; max-height: 400px; height: auto; cursor: pointer; border-radius: 4px; display: block; margin-bottom: 1em; }}
#             .post {{ margin-bottom: 1.5em; padding: 1em; border-radius: 8px; transition: background-color 0.3s, border-color 0.3s; }}
#             .post-header {{ font-size: 0.9em; margin-bottom: 0.5em; }}
#             .post-comment {{ word-wrap: break-word; font-size: 1em; line-height: 1.5; }}
#             .theme-toggle-button {{ position: fixed; top: 15px; right: 15px; padding: 8px 12px; border-radius: 20px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s, color 0.3s; }}
#             footer {{ text-align: center; margin-top: 2em; padding-top: 1em; border-top: 1px solid #ccc; font-size: 0.8em; color: #888; }}
#             body.light-theme {{ background-color: #f0f2f5; color: #1c1e21; }}
#             .light-theme .post {{ background-color: #ffffff; border: 1px solid #dddfe2; }} .light-theme a {{ color: #0d86ff; }} .light-theme .post-header {{ color: #606770; }} .light-theme .post-header .post-id {{ color: #d00; font-weight: bold; }} .light-theme .theme-toggle-button {{ background-color: #333; color: #fff; }}
#             body.dark-theme {{ background-color: #18191a; color: #e4e6eb; }}
#             .dark-theme .post {{ background-color: #242526; border: 1px solid #3a3b3c; }} .dark-theme a {{ color: #45abff; }} .dark-theme .post-header {{ color: #b0b3b8; }} .dark-theme .post-header .post-id {{ color: #ff6347; font-weight: bold; }} .dark-theme .theme-toggle-button {{ background-color: #eee; color: #111; }} .dark-theme footer {{ border-top-color: #3a3b3c; color: #6d6d6d; }}
#             .quote {{ color: #789922; }}
#         </style>
#     </head>
#     <body class="{initial_theme}-theme">
#         <button id="theme-toggle" class="theme-toggle-button">Cambiar Tema</button>
#         <div class="container">
#             <h1><a href="{thread.url}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
#     """
    
#     # Crear un conjunto para rastrear archivos ya utilizados
#     used_files = set()
#     available_files = list(downloaded_files)
    
#     for post in thread.all_posts:
#         html_content += f"""
#             <div class="post">
#                 <div class="post-header"><span class="post-id">Anónimo No.{post.post_id}</span> - <span>{post.datetime.strftime('%Y-%m-%d %H:%M:%S')}</span></div>
#                 <div class="post-comment">
#         """
#         if post.has_file and post.file:
#             actual_filename = None
            
#             # Buscar archivos no utilizados que coincidan con este post
#             remaining_files = [f for f in available_files if f not in used_files]
            
#             # Estrategia 1: Coincidencia exacta por nombre de archivo
#             for downloaded_file in remaining_files:
#                 if post.file.filename in downloaded_file and post.file.file_extension.lower() in downloaded_file.lower():
#                     actual_filename = downloaded_file
#                     break
            
#             # Estrategia 2: Coincidencia por extensión y orden cronológico
#             if not actual_filename:
#                 for downloaded_file in remaining_files:
#                     file_extension = os.path.splitext(downloaded_file)[1].lower()
#                     if file_extension == post.file.file_extension.lower():
#                         actual_filename = downloaded_file
#                         break
            
#             # Estrategia 3: Fallback - usar cualquier archivo disponible con extensión compatible
#             if not actual_filename:
#                 image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
#                 video_extensions = ['.webm', '.mp4', '.mov']
                
#                 post_ext = post.file.file_extension.lower()
                
#                 for downloaded_file in remaining_files:
#                     file_ext = os.path.splitext(downloaded_file)[1].lower()
                    
#                     # Si el post es una imagen, buscar cualquier imagen
#                     if post_ext in image_extensions and file_ext in image_extensions:
#                         actual_filename = downloaded_file
#                         break
#                     # Si el post es un video, buscar cualquier video
#                     elif post_ext in video_extensions and file_ext in video_extensions:
#                         actual_filename = downloaded_file
#                         break
            
#             if actual_filename:
#                 # Marcar este archivo como utilizado
#                 used_files.add(actual_filename)
                
#                 file_path_relative = f"{MEDIA_SUBFOLDER}/{actual_filename}"
#                 file_extension = os.path.splitext(actual_filename)[1].lower()
#                 if file_extension in ['.webm', '.mp4', '.mov']:
#                     html_content += f"""<video controls muted loop preload="metadata"><source src="{file_path_relative}" type="video/{file_extension[1:]}"></video>"""
#                 else:
#                     html_content += f'<a href="{file_path_relative}" target="_blank"><img src="{file_path_relative}" alt="{actual_filename}"></a>'
#             else:
#                 # Mostrar información de debug solo si realmente no hay archivos disponibles
#                 if remaining_files:
#                     expected_name = f"{post.file.filename}{post.file.file_extension}"
#                     html_content += f'<p><i>(Archivo {expected_name} no coincide con archivos restantes: {remaining_files})</i></p>'
#                 else:
#                     html_content += f'<p><i>(No hay más archivos disponibles para este post)</i></p>'
        
#         html_content += post.comment
#         html_content += "</div></div>"

#     html_content += f"""
#         <footer>Generado por 4chan Downloader v16.1 el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</footer>
#         </div>
#         <script>
#             const themeToggle = document.getElementById('theme-toggle'); const body = document.body;
#             const applyTheme = (theme) => {{ body.className = theme + '-theme'; themeToggle.textContent = theme === 'light' ? '🌙 Modo Noche' : '☀️ Modo Día'; localStorage.setItem('theme', theme); }};
#             themeToggle.addEventListener('click', () => {{ const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light'; applyTheme(newTheme); }});
#             const savedTheme = localStorage.getItem('theme') || '{initial_theme}'; applyTheme(savedTheme);
#         </script>
#     </body></html>
#     """
#     return html_content

# def download_thread(board_name, thread_id, theme='light', overwrite=False):
#     """Orquesta la descarga usando la arquitectura híbrida y robusta."""
#     try:
#         board = basc_py4chan.Board(board_name)
#         thread = board.get_thread(thread_id)
#         if not thread:
#             Console.print_warning(f"El hilo {thread_id} en /{board_name}/ ya no existe. Saltando.")
#             return None
        
#         thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
#         sanitized_subject = sanitize_filename(thread_subject)
        
#         folder_name = f"{thread_id}_{sanitized_subject}"
#         thread_folder = os.path.join(BASE_DOWNLOAD_DIR, board_name, folder_name)
#         media_folder = os.path.join(thread_folder, MEDIA_SUBFOLDER)
#         os.makedirs(media_folder, exist_ok=True)
        
#         Console.print_info(f"    > Iniciando descarga de medios con gallery-dl en '{media_folder}'...")
        
#         command = [
#             'gallery-dl',
#             '--directory', media_folder,
#             '-o', 'path=.',
#             '-o', 'filename={filename}.{extension}',
#             thread.url
#         ]
#         if overwrite: command.append('--no-skip')

#         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
#         for line in iter(process.stdout.readline, ''): print("      " + line, end='')
#         process.wait()

#         if process.returncode != 0:
#             Console.print_warning(f"    > gallery-dl finalizó con errores (código: {process.returncode}).")
#         else:
#             Console.print_success(f"    > Descarga de medios completada.")

#         Console.print_info("    > Verificando archivos descargados para construir el HTML...")
#         try:
#             downloaded_files_list = os.listdir(media_folder)
#             downloaded_files = set(downloaded_files_list)
#             Console.print_info(f"    > Archivos encontrados: {len(downloaded_files)}")
#             Console.print_info(f"    > Archivos descargados: {downloaded_files_list}")
#         except FileNotFoundError:
#             Console.print_warning("    > No se encontró la carpeta de medios.")
#             downloaded_files = set()

#         html_content = create_thread_html(thread, board_name, thread_id, thread_subject, downloaded_files, theme)
#         html_filename = f"{thread_id}_{sanitized_subject}.html"
#         html_path = os.path.join(thread_folder, html_filename)
        
#         with open(html_path, "w", encoding="utf-8") as f:
#             f.write(html_content)
#             Console.print_success(f"    > HTML guardado en: {html_path}")

#         return {"id": thread_id, "subject": thread_subject}

#     # CORRECCIÓN: Manejar excepciones de manera genérica
#     except Exception as e:
#         if '404' in str(e):
#             Console.print_warning(f"El hilo https://boards.4chan.org/{board_name}/thread/{thread_id} no fue encontrado (404).")
#         else:
#             Console.print_error(f"Error al procesar el hilo {thread_id}: {str(e)}")
#         import traceback
#         Console.print_error(traceback.format_exc())
#         return None

# def download_board(board_name, theme='light', overwrite=False, multithread=False):
#     try:
#         board = basc_py4chan.Board(board_name)
#         all_thread_ids = board.get_all_thread_ids()
#     except Exception as e:
#         Console.print_error(f"Error: No se pudo obtener la lista de hilos de /{board_name}/: {e}")
#         return
    
#     results = []
#     if multithread:
#         Console.print_info(f"Iniciando descarga en modo MULTI-HILO ({MAX_WORKERS} hilos)...")
#         with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#             args = [(board_name, thread_id, theme, overwrite) for thread_id in all_thread_ids]
#             results = list(tqdm(executor.map(lambda p: download_thread(*p), args), total=len(all_thread_ids), desc=f"Procesando /{board_name}/ (Multi-hilo)"))
#     else:
#         Console.print_info(f"Iniciando descarga en modo SECUENCIAL para {len(all_thread_ids)} hilos...")
#         for thread_id in tqdm(all_thread_ids, desc=f"Procesando /{board_name}/ (Secuencial)"):
#             results.append(download_thread(board_name, thread_id, theme, overwrite))

#     success_count = sum(1 for r in results if r is not None)
#     fail_count = len(results) - success_count
#     Console.print_info("\n----- RESUMEN DEL PROCESO -----")
#     Console.print_success(f"Hilos procesados con éxito: {success_count}")
#     Console.print_warning(f"Hilos fallidos o saltados: {fail_count}")
#     Console.print_info("-----------------------------")

# def main():
#     """Función principal con argparse."""
#     parser = argparse.ArgumentParser(
#         description="Descargador de hilos de 4chan. v16.0 - Corrección final de nombres de archivo.",
#         formatter_class=argparse.RawTextHelpFormatter)
#     parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
#     parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', help="Tema inicial para el HTML.")
#     parser.add_argument("--overwrite", action="store_true", help="Fuerza la re-verificación de archivos con gallery-dl.")
#     parser.add_argument("-mt", "--multithread", action="store_true", help="Activa el procesamiento multi-hilo para foros.")
#     args = parser.parse_args()

#     check_dependencies()

#     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
#     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)

#     if thread_match:
#         board_name, thread_id = thread_match.groups()
#         thread_id = int(thread_id)
#         download_thread(board_name, thread_id, args.tema, args.overwrite)
#     elif board_match:
#         board_name = board_match.group(1)
#         download_board(board_name, args.tema, args.overwrite, args.multithread)
#     else:
#         Console.print_error("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# if __name__ == "__main__":
#     main()

# v15
import basc_py4chan
import os
import sys
import re
import argparse
import subprocess
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# --- Constantes y Configuración Global ---
BASE_DOWNLOAD_DIR = "4chan_downloader"
MEDIA_SUBFOLDER = "media"  # Nombre de la subcarpeta para imágenes y videos
MAX_WORKERS = 5

class Console:
    """Clase para imprimir mensajes con colores en la consola."""
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    @staticmethod
    def print_success(message): print(f"{Console.OKGREEN}{message}{Console.ENDC}")
    @staticmethod
    def print_warning(message): print(f"{Console.WARNING}{message}{Console.ENDC}")
    @staticmethod
    def print_error(message): print(f"{Console.FAIL}{message}{Console.ENDC}", file=sys.stderr)
    @staticmethod
    def print_info(message): print(message)

def check_dependencies():
    """Verifica si las dependencias externas (gallery-dl) están instaladas."""
    if not shutil.which("gallery-dl"):
        Console.print_error("[ERROR CRÍTICO] El comando 'gallery-dl' no fue encontrado.")
        Console.print_error("Por favor, asegúrate de que gallery-dl esté instalado: pip install gallery-dl")
        sys.exit(1)
    Console.print_success("Dependencia 'gallery-dl' encontrada.")

def sanitize_filename(name):
    """Limpia un string para que sea un nombre de archivo/carpeta válido."""
    sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
    sanitized_name = sanitized_name.replace(" ", "_")
    return sanitized_name[:100]

def create_thread_html(thread, board_name, thread_id, thread_subject, downloaded_files, initial_theme='light'):
    """
    Genera el HTML usando basc-py4chan para el texto y una lista de archivos verificados en disco.
    Las rutas ahora apuntan a la subcarpeta MEDIA_SUBFOLDER.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{board_name} - {thread_subject} ({thread_id})</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 1em; line-height: 1.6; transition: background-color 0.3s, color 0.3s; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 1em; }}
            a {{ text-decoration: none; }} a:hover {{ text-decoration: underline; }}
            img, video {{ max-width: 350px; max-height: 400px; height: auto; cursor: pointer; border-radius: 4px; display: block; margin-bottom: 1em; }}
            .post {{ margin-bottom: 1.5em; padding: 1em; border-radius: 8px; transition: background-color 0.3s, border-color 0.3s; }}
            .post-header {{ font-size: 0.9em; margin-bottom: 0.5em; }}
            .post-comment {{ word-wrap: break-word; font-size: 1em; line-height: 1.5; }}
            .theme-toggle-button {{ position: fixed; top: 15px; right: 15px; padding: 8px 12px; border-radius: 20px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s, color 0.3s; }}
            footer {{ text-align: center; margin-top: 2em; padding-top: 1em; border-top: 1px solid #ccc; font-size: 0.8em; color: #888; }}
            body.light-theme {{ background-color: #f0f2f5; color: #1c1e21; }}
            .light-theme .post {{ background-color: #ffffff; border: 1px solid #dddfe2; }} .light-theme a {{ color: #0d86ff; }} .light-theme .post-header {{ color: #606770; }} .light-theme .post-header .post-id {{ color: #d00; font-weight: bold; }} .light-theme .theme-toggle-button {{ background-color: #333; color: #fff; }}
            body.dark-theme {{ background-color: #18191a; color: #e4e6eb; }}
            .dark-theme .post {{ background-color: #242526; border: 1px solid #3a3b3c; }} .dark-theme a {{ color: #45abff; }} .dark-theme .post-header {{ color: #b0b3b8; }} .dark-theme .post-header .post-id {{ color: #ff6347; font-weight: bold; }} .dark-theme .theme-toggle-button {{ background-color: #eee; color: #111; }} .dark-theme footer {{ border-top-color: #3a3b3c; color: #6d6d6d; }}
            .quote {{ color: #789922; }}
        </style>
    </head>
    <body class="{initial_theme}-theme">
        <button id="theme-toggle" class="theme-toggle-button">Cambiar Tema</button>
        <div class="container">
            <h1><a href="{thread.url}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
    """
    
    # Crear un conjunto para rastrear archivos ya utilizados
    used_files = set()
    available_files = list(downloaded_files)
    
    for post in thread.all_posts:
        html_content += f"""
            <div class="post">
                <div class="post-header"><span class="post-id">Anónimo No.{post.post_id}</span> - <span>{post.datetime.strftime('%Y-%m-%d %H:%M:%S')}</span></div>
                <div class="post-comment">
        """
        if post.has_file and post.file:
            actual_filename = None
            
            # Buscar archivos no utilizados que coincidan con este post
            remaining_files = [f for f in available_files if f not in used_files]
            
            # Estrategia 1: Coincidencia exacta por nombre de archivo
            for downloaded_file in remaining_files:
                if post.file.filename in downloaded_file and post.file.file_extension.lower() in downloaded_file.lower():
                    actual_filename = downloaded_file
                    break
            
            # Estrategia 2: Coincidencia por extensión y orden cronológico
            if not actual_filename:
                for downloaded_file in remaining_files:
                    file_extension = os.path.splitext(downloaded_file)[1].lower()
                    if file_extension == post.file.file_extension.lower():
                        actual_filename = downloaded_file
                        break
            
            # Estrategia 3: Fallback - usar cualquier archivo disponible con extensión compatible
            if not actual_filename:
                image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                video_extensions = ['.webm', '.mp4', '.mov']
                
                post_ext = post.file.file_extension.lower()
                
                for downloaded_file in remaining_files:
                    file_ext = os.path.splitext(downloaded_file)[1].lower()
                    
                    # Si el post es una imagen, buscar cualquier imagen
                    if post_ext in image_extensions and file_ext in image_extensions:
                        actual_filename = downloaded_file
                        break
                    # Si el post es un video, buscar cualquier video
                    elif post_ext in video_extensions and file_ext in video_extensions:
                        actual_filename = downloaded_file
                        break
            
            if actual_filename:
                # Marcar este archivo como utilizado
                used_files.add(actual_filename)
                
                file_path_relative = f"{MEDIA_SUBFOLDER}/{actual_filename}"
                file_extension = os.path.splitext(actual_filename)[1].lower()
                if file_extension in ['.webm', '.mp4', '.mov']:
                    html_content += f"""<video controls muted loop preload="metadata"><source src="{file_path_relative}" type="video/{file_extension[1:]}"></video>"""
                else:
                    html_content += f'<a href="{file_path_relative}" target="_blank"><img src="{file_path_relative}" alt="{actual_filename}"></a>'
            else:
                # Mostrar información de debug solo si realmente no hay archivos disponibles
                if remaining_files:
                    expected_name = f"{post.file.filename}{post.file.file_extension}"
                    html_content += f'<p><i>(Archivo {expected_name} no coincide con archivos restantes: {remaining_files})</i></p>'
                else:
                    html_content += f'<p><i>(No hay más archivos disponibles para este post)</i></p>'
        
        html_content += post.comment
        html_content += "</div></div>"

    html_content += f"""
        <footer>Generado por 4chan Downloader v16.1 el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</footer>
        </div>
        <script>
            const themeToggle = document.getElementById('theme-toggle'); const body = document.body;
            const applyTheme = (theme) => {{ body.className = theme + '-theme'; themeToggle.textContent = theme === 'light' ? '🌙 Modo Noche' : '☀️ Modo Día'; localStorage.setItem('theme', theme); }};
            themeToggle.addEventListener('click', () => {{ const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light'; applyTheme(newTheme); }});
            const savedTheme = localStorage.getItem('theme') || '{initial_theme}'; applyTheme(savedTheme);
        </script>
    </body></html>
    """
    return html_content

def download_thread(board_name, thread_id, theme='light', overwrite=False, sleep_time=0):
    """Orquesta la descarga usando la arquitectura híbrida y robusta."""
    try:
        board = basc_py4chan.Board(board_name)
        thread = board.get_thread(thread_id)
        if not thread:
            Console.print_warning(f"El hilo {thread_id} en /{board_name}/ ya no existe. Saltando.")
            return None
        
        thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
        sanitized_subject = sanitize_filename(thread_subject)
        
        folder_name = f"{thread_id}_{sanitized_subject}"
        thread_folder = os.path.join(BASE_DOWNLOAD_DIR, board_name, folder_name)
        media_folder = os.path.join(thread_folder, MEDIA_SUBFOLDER)
        os.makedirs(media_folder, exist_ok=True)
        
        Console.print_info(f"    > Iniciando descarga de medios con gallery-dl en '{media_folder}'...")
        
        command = [
            'gallery-dl',
            '--directory', media_folder,
            '-o', 'path=.',
            '-o', 'filename={filename}.{extension}',
        ]
        
        # Agregar sleep si se especifica
        if sleep_time > 0:
            command.extend(['--sleep', str(sleep_time)])
            Console.print_info(f"    > Usando delay de {sleep_time} segundos entre descargas...")
        
        command.append(thread.url)
        
        if overwrite: 
            command.insert(-1, '--no-skip')  # Insertar antes de la URL

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        for line in iter(process.stdout.readline, ''): print("      " + line, end='')
        process.wait()

        if process.returncode != 0:
            Console.print_warning(f"    > gallery-dl finalizó con errores (código: {process.returncode}).")
        else:
            Console.print_success(f"    > Descarga de medios completada.")

        Console.print_info("    > Verificando archivos descargados para construir el HTML...")
        try:
            downloaded_files_list = os.listdir(media_folder)
            downloaded_files = set(downloaded_files_list)
            Console.print_info(f"    > Archivos encontrados: {len(downloaded_files)}")
            Console.print_info(f"    > Archivos descargados: {downloaded_files_list}")
        except FileNotFoundError:
            Console.print_warning("    > No se encontró la carpeta de medios.")
            downloaded_files = set()

        html_content = create_thread_html(thread, board_name, thread_id, thread_subject, downloaded_files, theme)
        html_filename = f"{thread_id}_{sanitized_subject}.html"
        html_path = os.path.join(thread_folder, html_filename)
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            Console.print_success(f"    > HTML guardado en: {html_path}")

        return {"id": thread_id, "subject": thread_subject}

    # CORRECCIÓN: Manejar excepciones de manera genérica
    except Exception as e:
        if '404' in str(e):
            Console.print_warning(f"El hilo https://boards.4chan.org/{board_name}/thread/{thread_id} no fue encontrado (404).")
        else:
            Console.print_error(f"Error al procesar el hilo {thread_id}: {str(e)}")
        import traceback
        Console.print_error(traceback.format_exc())
        return None

def download_board(board_name, theme='light', overwrite=False, multithread=False, sleep_time=0):
    try:
        board = basc_py4chan.Board(board_name)
        all_thread_ids = board.get_all_thread_ids()
    except Exception as e:
        Console.print_error(f"Error: No se pudo obtener la lista de hilos de /{board_name}/: {e}")
        return
    
    results = []
    if multithread:
        Console.print_info(f"Iniciando descarga en modo MULTI-HILO ({MAX_WORKERS} hilos)...")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            args = [(board_name, thread_id, theme, overwrite, sleep_time) for thread_id in all_thread_ids]
            results = list(tqdm(executor.map(lambda p: download_thread(*p), args), total=len(all_thread_ids), desc=f"Procesando /{board_name}/ (Multi-hilo)"))
    else:
        Console.print_info(f"Iniciando descarga en modo SECUENCIAL para {len(all_thread_ids)} hilos...")
        for thread_id in tqdm(all_thread_ids, desc=f"Procesando /{board_name}/ (Secuencial)"):
            results.append(download_thread(board_name, thread_id, theme, overwrite, sleep_time))

    success_count = sum(1 for r in results if r is not None)
    fail_count = len(results) - success_count
    Console.print_info("\n----- RESUMEN DEL PROCESO -----")
    Console.print_success(f"Hilos procesados con éxito: {success_count}")
    Console.print_warning(f"Hilos fallidos o saltados: {fail_count}")
    Console.print_info("-----------------------------")

def main():
    """Función principal con argparse."""
    parser = argparse.ArgumentParser(
        description="Descargador de hilos de 4chan. v16.1 - Con soporte para delay entre descargas.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
    parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', help="Tema inicial para el HTML.")
    parser.add_argument("--overwrite", action="store_true", help="Fuerza la re-verificación de archivos con gallery-dl.")
    parser.add_argument("-mt", "--multithread", action="store_true", help="Activa el procesamiento multi-hilo para foros.")
    parser.add_argument("-s", "--sleep", type=float, default=0, metavar="SECONDS", 
                       help="Tiempo de espera en segundos entre descargas (ej: 1.5). Útil para evitar bans.")
    args = parser.parse_args()

    check_dependencies()

    if args.sleep > 0:
        Console.print_info(f"Configurado delay de {args.sleep} segundos entre descargas.")

    board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
    thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)

    if thread_match:
        board_name, thread_id = thread_match.groups()
        thread_id = int(thread_id)
        download_thread(board_name, thread_id, args.tema, args.overwrite, args.sleep)
    elif board_match:
        board_name = board_match.group(1)
        download_board(board_name, args.tema, args.overwrite, args.multithread, args.sleep)
    else:
        Console.print_error("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

if __name__ == "__main__":
    main()