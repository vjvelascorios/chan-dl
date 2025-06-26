# # # # # # # # import basc_py4chan
# # # # # # # # import requests
# # # # # # # # import os
# # # # # # # # import sys
# # # # # # # # import re
# # # # # # # # from datetime import datetime

# # # # # # # # def download_file(url, folder):
# # # # # # # #     """Descarga un archivo desde una URL a una carpeta específica."""
# # # # # # # #     if not os.path.exists(folder):
# # # # # # # #         os.makedirs(folder)
# # # # # # # #     try:
# # # # # # # #         response = requests.get(url, stream=True)
# # # # # # # #         response.raise_for_status()
# # # # # # # #         filename = os.path.join(folder, url.split('/')[-1])
# # # # # # # #         with open(filename, 'wb') as f:
# # # # # # # #             for chunk in response.iter_content(chunk_size=8192):
# # # # # # # #                 f.write(chunk)
# # # # # # # #         return filename
# # # # # # # #     except requests.exceptions.RequestException as e:
# # # # # # # #         print(f"Error al descargar {url}: {e}")
# # # # # # # #         return None

# # # # # # # # def create_thread_html(thread, board_name, thread_id):
# # # # # # # #     """Crea un archivo HTML para un hilo descargado."""
# # # # # # # #     html_content = f"""
# # # # # # # #     <!DOCTYPE html>
# # # # # # # #     <html>
# # # # # # # #     <head>
# # # # # # # #         <title>{board_name} - Hilo {thread_id}</title>
# # # # # # # #         <style>
# # # # # # # #             body {{ font-family: sans-serif; margin: 2em; }}
# # # # # # # #             .post {{ border: 1px solid #ccc; margin-bottom: 1em; padding: 1em; }}
# # # # # # # #             .post-header {{ font-weight: bold; }}
# # # # # # # #             .post-comment {{ margin-top: 1em; }}
# # # # # # # #             img {{ max-width: 100%; height: auto; }}
# # # # # # # #         </style>
# # # # # # # #     </head>
# # # # # # # #     <body>
# # # # # # # #         <h1><a href="https://boards.4chan.org/{board_name}/thread/{thread_id}" target="_blank">/{board_name}/ - Hilo {thread_id}</a></h1>
# # # # # # # #     """

# # # # # # # #     for post in thread.all_posts:
# # # # # # # #         html_content += f"""
# # # # # # # #         <div class="post">
# # # # # # # #             <div class="post-header">
# # # # # # # #                 Anónimo No.{post.post_id} - {datetime.fromtimestamp(post.timestamp)}
# # # # # # # #             </div>
# # # # # # # #             <div class="post-comment">
# # # # # # # #         """
# # # # # # # #         if post.has_file:
# # # # # # # #             image_name = post.file_url.split('/')[-1]
# # # # # # # #             html_content += f'<a href="images/{image_name}" target="_blank"><img src="images/{image_name}"></a><br>'

# # # # # # # #         html_content += post.comment
# # # # # # # #         html_content += """
# # # # # # # #             </div>
# # # # # # # #         </div>
# # # # # # # #         """

# # # # # # # #     html_content += """
# # # # # # # #     </body>
# # # # # # # #     </html>
# # # # # # # #     """
# # # # # # # #     return html_content

# # # # # # # # def download_thread(board_name, thread_id):
# # # # # # # #     """Descarga un hilo completo, incluyendo imágenes y generando un archivo HTML."""
# # # # # # # #     try:
# # # # # # # #         board = basc_py4chan.Board(board_name)
# # # # # # # #         thread = board.get_thread(thread_id)
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"No se pudo obtener el hilo {thread_id} de /{board_name}/: {e}")
# # # # # # # #         return

# # # # # # # #     if not thread:
# # # # # # # #         print(f"El hilo {thread_id} en /{board_name}/ no existe o fue eliminado.")
# # # # # # # #         return

# # # # # # # #     print(f"Descargando hilo {thread_id} de /{board_name}/...")
# # # # # # # #     thread_folder = os.path.join("4chan_downloader", board_name, str(thread_id))
# # # # # # # #     images_folder = os.path.join(thread_folder, "images")

# # # # # # # #     if not os.path.exists(images_folder):
# # # # # # # #         os.makedirs(images_folder)

# # # # # # # #     for post in thread.all_posts:
# # # # # # # #         if post.has_file:
# # # # # # # #             download_file(post.file_url, images_folder)

# # # # # # # #     html_content = create_thread_html(thread, board_name, thread_id)
# # # # # # # #     with open(os.path.join(thread_folder, f"{thread_id}.html"), "w", encoding="utf-8") as f:
# # # # # # # #         f.write(html_content)

# # # # # # # #     print(f"Hilo {thread_id} de /{board_name}/ descargado en: {thread_folder}")

# # # # # # # # def download_board(board_name):
# # # # # # # #     """Descarga todos los hilos de un foro."""
# # # # # # # #     try:
# # # # # # # #         board = basc_py4chan.Board(board_name)
# # # # # # # #         all_thread_ids = board.get_all_thread_ids()
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"No se pudo obtener la lista de hilos de /{board_name}/: {e}")
# # # # # # # #         return

# # # # # # # #     print(f"Se encontraron {len(all_thread_ids)} hilos en /{board_name}/. Comenzando la descarga...")

# # # # # # # #     for thread_id in all_thread_ids:
# # # # # # # #         download_thread(board_name, thread_id)

# # # # # # # # def main():
# # # # # # # #     """Función principal que procesa la URL de entrada."""
# # # # # # # #     if len(sys.argv) != 2:
# # # # # # # #         print("Uso: python 4chan_downloader.py <URL_de_4chan>")
# # # # # # # #         return

# # # # # # # #     url = sys.argv[1]
# # # # # # # #     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", url)
# # # # # # # #     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", url)

# # # # # # # #     if thread_match:
# # # # # # # #         board_name = thread_match.group(1)
# # # # # # # #         thread_id = int(thread_match.group(2))
# # # # # # # #         download_thread(board_name, thread_id)
# # # # # # # #     elif board_match:
# # # # # # # #         board_name = board_match.group(1)
# # # # # # # #         download_board(board_name)
# # # # # # # #     else:
# # # # # # # #         print("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# # # # # # # # if __name__ == "__main__":
# # # # # # # #     main()



# # # # # # # import basc_py4chan
# # # # # # # import requests
# # # # # # # import os
# # # # # # # import sys
# # # # # # # import re
# # # # # # # from datetime import datetime

# # # # # # # # NUEVO: Función para limpiar y crear un nombre de carpeta válido a partir de un texto.
# # # # # # # def sanitize_filename(name):
# # # # # # #     """
# # # # # # #     Elimina los caracteres inválidos de un string para que pueda ser usado
# # # # # # #     como nombre de archivo o carpeta.
# # # # # # #     """
# # # # # # #     # Elimina caracteres prohibidos en la mayoría de sistemas de archivos
# # # # # # #     sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
# # # # # # #     # Reemplaza espacios con guiones bajos para mejor legibilidad
# # # # # # #     sanitized_name = sanitized_name.replace(" ", "_")
# # # # # # #     # Trunca el nombre si es demasiado largo para evitar problemas en el sistema de archivos
# # # # # # #     return sanitized_name[:100]

# # # # # # # def download_file(url, folder):
# # # # # # #     """Descarga un archivo desde una URL a una carpeta específica."""
# # # # # # #     if not os.path.exists(folder):
# # # # # # #         os.makedirs(folder)
# # # # # # #     try:
# # # # # # #         response = requests.get(url, stream=True)
# # # # # # #         response.raise_for_status()
# # # # # # #         filename = os.path.join(folder, url.split('/')[-1])
# # # # # # #         with open(filename, 'wb') as f:
# # # # # # #             for chunk in response.iter_content(chunk_size=8192):
# # # # # # #                 f.write(chunk)
# # # # # # #             return filename
# # # # # # #     except requests.exceptions.RequestException as e:
# # # # # # #         print(f"Error al descargar {url}: {e}")
# # # # # # #         return None

# # # # # # # def create_thread_html(thread, board_name, thread_id, thread_subject):
# # # # # # #     """Crea un archivo HTML para un hilo descargado."""
# # # # # # #     html_content = f"""
# # # # # # #     <!DOCTYPE html>
# # # # # # #     <html>
# # # # # # #     <head>
# # # # # # #         <title>{board_name} - {thread_subject} ({thread_id})</title>
# # # # # # #         <style>
# # # # # # #             body {{ font-family: sans-serif; margin: 2em; background-color: #f0f0f0; color: #333; }}
# # # # # # #             h1 a {{ color: #d00; text-decoration: none; }}
# # # # # # #             h1 a:hover {{ text-decoration: underline; }}
# # # # # # #             .post {{ border: 1px solid #ccc; margin-bottom: 1em; padding: 1em; background-color: #fff; border-radius: 5px; }}
# # # # # # #             .post-header {{ font-weight: bold; color: #d00; }}
# # # # # # #             .post-comment {{ margin-top: 1em; word-wrap: break-word; }}
# # # # # # #             img {{ max-width: 250px; height: auto; cursor: pointer; border: 1px solid #ddd; }}
# # # # # # #         </style>
# # # # # # #     </head>
# # # # # # #     <body>
# # # # # # #         <h1><a href="https://boards.4chan.org/{board_name}/thread/{thread_id}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
# # # # # # #     """

# # # # # # #     for post in thread.all_posts:
# # # # # # #         html_content += f"""
# # # # # # #         <div class="post">
# # # # # # #             <div class="post-header">
# # # # # # #                 Anónimo No.{post.post_id} - {datetime.fromtimestamp(post.timestamp)}
# # # # # # #             </div>
# # # # # # #             <div class="post-comment">
# # # # # # #         """
# # # # # # #         if post.has_file:
# # # # # # #             image_name = post.file_url.split('/')[-1]
# # # # # # #             html_content += f'<a href="images/{image_name}" target="_blank"><img src="images/{image_name}" alt="{image_name}"></a><br><br>'

# # # # # # #         # MODIFICADO: Se reemplazan los saltos de línea del comentario para que se muestren en HTML
# # # # # # #         comment_html = post.comment.replace('\n', '<br>')
# # # # # # #         html_content += comment_html
# # # # # # #         html_content += """
# # # # # # #             </div>
# # # # # # #         </div>
# # # # # # #         """

# # # # # # #     html_content += """
# # # # # # #     </body>
# # # # # # #     </html>
# # # # # # #     """
# # # # # # #     return html_content

# # # # # # # def download_thread(board_name, thread_id):
# # # # # # #     """Descarga un hilo completo, incluyendo imágenes y generando un archivo HTML."""
# # # # # # #     try:
# # # # # # #         board = basc_py4chan.Board(board_name)
# # # # # # #         thread = board.get_thread(thread_id)
# # # # # # #     except Exception as e:
# # # # # # #         print(f"No se pudo obtener el hilo {thread_id} de /{board_name}/: {e}")
# # # # # # #         return

# # # # # # #     if not thread:
# # # # # # #         print(f"El hilo {thread_id} en /{board_name}/ no existe o fue eliminado.")
# # # # # # #         return

# # # # # # #     # NUEVO: Obtener el asunto del hilo y sanitizarlo.
# # # # # # #     # Si no hay asunto, se usa un nombre genérico.
# # # # # # #     thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
# # # # # # #     sanitized_subject = sanitize_filename(thread_subject)

# # # # # # #     print(f"Descargando hilo: '{thread_subject}' ({thread_id}) de /{board_name}/...")

# # # # # # #     # MODIFICADO: Se crea el nombre de la carpeta usando el ID y el asunto sanitizado.
# # # # # # #     folder_name = f"{thread_id}_{sanitized_subject}"
# # # # # # #     thread_folder = os.path.join("4chan_downloader", board_name, folder_name)
# # # # # # #     images_folder = os.path.join(thread_folder, "images")

# # # # # # #     if not os.path.exists(images_folder):
# # # # # # #         os.makedirs(images_folder)

# # # # # # #     for post in thread.all_posts:
# # # # # # #         if post.has_file:
# # # # # # #             download_file(post.file_url, images_folder)

# # # # # # #     # MODIFICADO: Se pasa el asunto del hilo a la función que crea el HTML.
# # # # # # #     html_content = create_thread_html(thread, board_name, thread_id, thread_subject)
# # # # # # #     # MODIFICADO: El archivo HTML ahora se nombra con el ID y el asunto.
# # # # # # #     html_filename = f"{thread_id}_{sanitized_subject}.html"
# # # # # # #     with open(os.path.join(thread_folder, html_filename), "w", encoding="utf-8") as f:
# # # # # # #         f.write(html_content)

# # # # # # #     print(f"Hilo '{thread_subject}' descargado en: {thread_folder}")

# # # # # # # def download_board(board_name):
# # # # # # #     """Descarga todos los hilos de un foro."""
# # # # # # #     try:
# # # # # # #         board = basc_py4chan.Board(board_name)
# # # # # # #         all_thread_ids = board.get_all_thread_ids()
# # # # # # #     except Exception as e:
# # # # # # #         print(f"No se pudo obtener la lista de hilos de /{board_name}/: {e}")
# # # # # # #         return

# # # # # # #     print(f"Se encontraron {len(all_thread_ids)} hilos en /{board_name}/. Comenzando la descarga...")

# # # # # # #     for thread_id in all_thread_ids:
# # # # # # #         download_thread(board_name, thread_id)
# # # # # # #         print("-" * 20) # Separador para mayor claridad

# # # # # # # def main():
# # # # # # #     """Función principal que procesa la URL de entrada."""
# # # # # # #     if len(sys.argv) != 2:
# # # # # # #         print("Uso: python 4chan_downloader_v2.py <URL_de_4chan>")
# # # # # # #         return

# # # # # # #     url = sys.argv[1]
# # # # # # #     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", url)
# # # # # # #     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", url)

# # # # # # #     if thread_match:
# # # # # # #         board_name = thread_match.group(1)
# # # # # # #         thread_id = int(thread_match.group(2))
# # # # # # #         download_thread(board_name, thread_id)
# # # # # # #     elif board_match:
# # # # # # #         board_name = board_match.group(1)
# # # # # # #         download_board(board_name)
# # # # # # #     else:
# # # # # # #         print("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# # # # # # # if __name__ == "__main__":
# # # # # # #     main()



# # # # # # import basc_py4chan
# # # # # # import requests
# # # # # # import os
# # # # # # import sys
# # # # # # import re
# # # # # # import argparse # NUEVO: Para un manejo de argumentos más profesional
# # # # # # from datetime import datetime
# # # # # # from concurrent.futures import ThreadPoolExecutor # NUEVO: Para descargas paralelas
# # # # # # from tqdm import tqdm # NUEVO: Para barras de progreso

# # # # # # def sanitize_filename(name):
# # # # # #     """Limpia un string para que sea un nombre de archivo/carpeta válido."""
# # # # # #     sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
# # # # # #     sanitized_name = sanitized_name.replace(" ", "_")
# # # # # #     return sanitized_name[:100]

# # # # # # def download_file(url, folder):
# # # # # #     """Descarga un archivo desde una URL a una carpeta específica."""
# # # # # #     if not os.path.exists(folder):
# # # # # #         os.makedirs(folder)
# # # # # #     try:
# # # # # #         response = requests.get(url, stream=True, timeout=10)
# # # # # #         response.raise_for_status()
# # # # # #         filename = os.path.join(folder, url.split('/')[-1])
# # # # # #         with open(filename, 'wb') as f:
# # # # # #             for chunk in response.iter_content(chunk_size=8192):
# # # # # #                 f.write(chunk)
# # # # # #         return filename
# # # # # #     except requests.exceptions.RequestException as e:
# # # # # #         # Silenciamos el error en consola para no ensuciar la barra de progreso
# # # # # #         pass # print(f"Error al descargar {url}: {e}")
# # # # # #         return None

# # # # # # def create_thread_html(thread, board_name, thread_id, thread_subject, initial_theme='light'):
# # # # # #     """
# # # # # #     NUEVO: Crea un archivo HTML para un hilo con un selector de tema (día/noche)
# # # # # #     integrado mediante CSS y JavaScript.
# # # # # #     """
    
# # # # # #     # El HTML ahora contiene el CSS para ambos temas y un script para cambiarlos.
# # # # # #     html_content = f"""
# # # # # #     <!DOCTYPE html>
# # # # # #     <html lang="es">
# # # # # #     <head>
# # # # # #         <meta charset="UTF-8">
# # # # # #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # # # #         <title>{board_name} - {thread_subject} ({thread_id})</title>
# # # # # #         <style>
# # # # # #             /* Estilos base */
# # # # # #             body {{
# # # # # #                 font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
# # # # # #                 margin: 0;
# # # # # #                 padding: 1em;
# # # # # #                 line-height: 1.6;
# # # # # #                 transition: background-color 0.3s, color 0.3s;
# # # # # #             }}
# # # # # #             .container {{ max-width: 800px; margin: 0 auto; padding: 1em; }}
# # # # # #             a {{ text-decoration: none; }}
# # # # # #             a:hover {{ text-decoration: underline; }}
# # # # # #             img {{ max-width: 250px; height: auto; cursor: pointer; border-radius: 4px; display: block; margin-bottom: 1em; }}
# # # # # #             .post {{ margin-bottom: 1.5em; padding: 1em; border-radius: 8px; transition: background-color 0.3s, border-color 0.3s; }}
# # # # # #             .post-header {{ font-size: 0.9em; margin-bottom: 0.5em; }}
# # # # # #             .post-comment {{ word-wrap: break-word; }}
# # # # # #             .theme-toggle-button {{
# # # # # #                 position: fixed; top: 15px; right: 15px; padding: 8px 12px;
# # # # # #                 border-radius: 20px; border: none; cursor: pointer; font-weight: bold;
# # # # # #                 box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s, color 0.3s;
# # # # # #             }}

# # # # # #             /* Tema Claro (Día) */
# # # # # #             body.light-theme {{
# # # # # #                 background-color: #f0f2f5; color: #1c1e21;
# # # # # #             }}
# # # # # #             .light-theme .post {{ background-color: #ffffff; border: 1px solid #dddfe2; }}
# # # # # #             .light-theme a {{ color: #0d86ff; }}
# # # # # #             .light-theme .post-header {{ color: #606770; }}
# # # # # #             .light-theme .post-header .post-id {{ color: #d00; font-weight: bold; }}
# # # # # #             .light-theme .theme-toggle-button {{ background-color: #333; color: #fff; }}

# # # # # #             /* Tema Oscuro (Noche) */
# # # # # #             body.dark-theme {{
# # # # # #                 background-color: #18191a; color: #e4e6eb;
# # # # # #             }}
# # # # # #             .dark-theme .post {{ background-color: #242526; border: 1px solid #3a3b3c; }}
# # # # # #             .dark-theme a {{ color: #45abff; }}
# # # # # #             .dark-theme .post-header {{ color: #b0b3b8; }}
# # # # # #             .dark-theme .post-header .post-id {{ color: #ff6347; font-weight: bold; }}
# # # # # #             .dark-theme .theme-toggle-button {{ background-color: #eee; color: #111; }}
# # # # # #         </style>
# # # # # #     </head>
# # # # # #     <body class="{initial_theme}-theme">
# # # # # #         <button id="theme-toggle" class="theme-toggle-button">Cambiar Tema</button>
# # # # # #         <div class="container">
# # # # # #             <h1><a href="https://boards.4chan.org/{board_name}/thread/{thread_id}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
# # # # # #     """

# # # # # #     for post in thread.all_posts:
# # # # # #         html_content += f"""
# # # # # #             <div class="post">
# # # # # #                 <div class="post-header">
# # # # # #                     <span class="post-id">Anónimo No.{post.post_id}</span> - <span>{datetime.fromtimestamp(post.timestamp)}</span>
# # # # # #                 </div>
# # # # # #                 <div class="post-comment">
# # # # # #         """
# # # # # #         if post.has_file:
# # # # # #             image_name = post.file_url.split('/')[-1]
# # # # # #             html_content += f'<a href="images/{image_name}" target="_blank"><img src="images/{image_name}" alt="{image_name}"></a>'

# # # # # #         comment_html = post.comment.replace('\n', '<br>')
# # # # # #         html_content += comment_html
# # # # # #         html_content += """
# # # # # #                 </div>
# # # # # #             </div>
# # # # # #         """

# # # # # #     html_content += """
# # # # # #         </div>
# # # # # #         <script>
# # # # # #             const themeToggle = document.getElementById('theme-toggle');
# # # # # #             const body = document.body;
            
# # # # # #             // Función para aplicar el tema
# # # # # #             const applyTheme = (theme) => {
# # # # # #                 body.className = theme + '-theme';
# # # # # #                 themeToggle.textContent = theme === 'light' ? '🌙 Modo Noche' : '☀️ Modo Día';
# # # # # #                 localStorage.setItem('theme', theme);
# # # # # #             };

# # # # # #             // Evento al hacer clic en el botón
# # # # # #             themeToggle.addEventListener('click', () => {
# # # # # #                 const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light';
# # # # # #                 applyTheme(newTheme);
# # # # # #             });

# # # # # #             // Cargar el tema guardado o el inicial
# # # # # #             const savedTheme = localStorage.getItem('theme') || '""" + initial_theme + """';
# # # # # #             applyTheme(savedTheme);
# # # # # #         </script>
# # # # # #     </body>
# # # # # #     </html>
# # # # # #     """
# # # # # #     return html_content

# # # # # # def download_thread(board_name, thread_id, theme='light'):
# # # # # #     """Descarga un hilo completo. Ahora acepta un argumento de tema."""
# # # # # #     try:
# # # # # #         board = basc_py4chan.Board(board_name)
# # # # # #         thread = board.get_thread(thread_id)
# # # # # #         if not thread: return
        
# # # # # #         thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
# # # # # #         sanitized_subject = sanitize_filename(thread_subject)
        
# # # # # #         folder_name = f"{thread_id}_{sanitized_subject}"
# # # # # #         thread_folder = os.path.join("4chan_downloader", board_name, folder_name)
# # # # # #         images_folder = os.path.join(thread_folder, "images")

# # # # # #         if not os.path.exists(images_folder):
# # # # # #             os.makedirs(images_folder)

# # # # # #         for post in thread.all_posts:
# # # # # #             if post.has_file:
# # # # # #                 download_file(post.file_url, images_folder)
        
# # # # # #         html_content = create_thread_html(thread, board_name, thread_id, thread_subject, theme)
# # # # # #         html_filename = f"{thread_id}_{sanitized_subject}.html"
# # # # # #         with open(os.path.join(thread_folder, html_filename), "w", encoding="utf-8") as f:
# # # # # #             f.write(html_content)

# # # # # #     except Exception as e:
# # # # # #         # No imprimir errores individuales para mantener limpia la salida de la barra de progreso
# # # # # #         pass
# # # # # #     return thread_id # Devuelve el ID para la barra de progreso


# # # # # # def download_board(board_name, theme='light'):
# # # # # #     """NUEVO: Descarga todos los hilos de un foro de forma concurrente con una barra de progreso."""
# # # # # #     try:
# # # # # #         board = basc_py4chan.Board(board_name)
# # # # # #         all_thread_ids = board.get_all_thread_ids()
# # # # # #     except Exception as e:
# # # # # #         print(f"Error: No se pudo obtener la lista de hilos de /{board_name}/: {e}")
# # # # # #         return

# # # # # #     # Usar un máximo de 10 trabajadores para no sobrecargar la API de 4chan
# # # # # #     # y limitar el número de hilos en máquinas con muchos núcleos.
# # # # # #     max_workers = min(10, os.cpu_count() + 4 if os.cpu_count() else 5)

# # # # # #     with ThreadPoolExecutor(max_workers=max_workers) as executor:
# # # # # #         # Preparamos los argumentos para cada llamada a download_thread
# # # # # #         args = [(board_name, thread_id, theme) for thread_id in all_thread_ids]
        
# # # # # #         # tqdm muestra la barra de progreso
# # # # # #         results = list(tqdm(executor.map(lambda p: download_thread(*p), args), 
# # # # # #                             total=len(all_thread_ids), 
# # # # # #                             desc=f"Descargando /{board_name}/"))
# # # # # #     print(f"\nDescarga del foro /{board_name}/ completada.")


# # # # # # def main():
# # # # # #     """NUEVO: Función principal con argparse para un manejo robusto de argumentos."""
# # # # # #     parser = argparse.ArgumentParser(
# # # # # #         description="Descarga hilos o foros completos de 4chan para verlos offline.",
# # # # # #         formatter_class=argparse.RawTextHelpFormatter,
# # # # # #         epilog="""Ejemplos de uso:
# # # # # #   python %(prog)s https://boards.4chan.org/wg/thread/1234567
# # # # # #   python %(prog)s https://boards.4chan.org/g/ --tema dark
# # # # # # """
# # # # # #     )
# # # # # #     parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
# # # # # #     parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', 
# # # # # #                         help="Elige el tema inicial para los archivos HTML (light o dark). Default: light.")
    
# # # # # #     args = parser.parse_args()

# # # # # #     url = args.url
# # # # # #     theme = args.tema
    
# # # # # #     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", url)
# # # # # #     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", url)

# # # # # #     if thread_match:
# # # # # #         board_name = thread_match.group(1)
# # # # # #         thread_id = int(thread_match.group(2))
# # # # # #         print(f"Iniciando descarga del hilo {thread_id} de /{board_name}/...")
# # # # # #         download_thread(board_name, thread_id, theme)
# # # # # #         print("Descarga completada.")
# # # # # #     elif board_match:
# # # # # #         board_name = board_match.group(1)
# # # # # #         download_board(board_name, theme)
# # # # # #     else:
# # # # # #         print("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# # # # # # if __name__ == "__main__":
# # # # # #     main()





# # # # # import basc_py4chan
# # # # # import requests
# # # # # import os
# # # # # import sys
# # # # # import re
# # # # # import argparse
# # # # # from datetime import datetime
# # # # # from concurrent.futures import ThreadPoolExecutor
# # # # # from tqdm import tqdm

# # # # # def sanitize_filename(name):
# # # # #     """Limpia un string para que sea un nombre de archivo/carpeta válido."""
# # # # #     sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
# # # # #     sanitized_name = sanitized_name.replace(" ", "_")
# # # # #     return sanitized_name[:100]

# # # # # def download_file(url, folder):
# # # # #     """Descarga un archivo desde una URL a una carpeta específica."""
# # # # #     try:
# # # # #         response = requests.get(url, stream=True, timeout=15)
# # # # #         response.raise_for_status()
# # # # #         filename = os.path.join(folder, url.split('/')[-1])
# # # # #         with open(filename, 'wb') as f:
# # # # #             for chunk in response.iter_content(chunk_size=8192):
# # # # #                 f.write(chunk)
# # # # #         return filename
# # # # #     except requests.exceptions.RequestException:
# # # # #         return None

# # # # # def create_thread_html(thread, board_name, thread_id, thread_subject, initial_theme='light'):
# # # # #     """Crea un archivo HTML para un hilo con un selector de tema (día/noche)."""
# # # # #     # (Esta función no necesita cambios respecto a la v3)
# # # # #     html_content = f"""
# # # # #     <!DOCTYPE html>
# # # # #     <html lang="es">
# # # # #     <head>
# # # # #         <meta charset="UTF-8">
# # # # #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # # #         <title>{board_name} - {thread_subject} ({thread_id})</title>
# # # # #         <style>
# # # # #             body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 1em; line-height: 1.6; transition: background-color 0.3s, color 0.3s; }}
# # # # #             .container {{ max-width: 800px; margin: 0 auto; padding: 1em; }}
# # # # #             a {{ text-decoration: none; }}
# # # # #             a:hover {{ text-decoration: underline; }}
# # # # #             img {{ max-width: 250px; height: auto; cursor: pointer; border-radius: 4px; display: block; margin-bottom: 1em; }}
# # # # #             .post {{ margin-bottom: 1.5em; padding: 1em; border-radius: 8px; transition: background-color 0.3s, border-color 0.3s; }}
# # # # #             .post-header {{ font-size: 0.9em; margin-bottom: 0.5em; }}
# # # # #             .post-comment {{ word-wrap: break-word; }}
# # # # #             .theme-toggle-button {{ position: fixed; top: 15px; right: 15px; padding: 8px 12px; border-radius: 20px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s, color 0.3s; }}
# # # # #             body.light-theme {{ background-color: #f0f2f5; color: #1c1e21; }}
# # # # #             .light-theme .post {{ background-color: #ffffff; border: 1px solid #dddfe2; }}
# # # # #             .light-theme a {{ color: #0d86ff; }}
# # # # #             .light-theme .post-header {{ color: #606770; }}
# # # # #             .light-theme .post-header .post-id {{ color: #d00; font-weight: bold; }}
# # # # #             .light-theme .theme-toggle-button {{ background-color: #333; color: #fff; }}
# # # # #             body.dark-theme {{ background-color: #18191a; color: #e4e6eb; }}
# # # # #             .dark-theme .post {{ background-color: #242526; border: 1px solid #3a3b3c; }}
# # # # #             .dark-theme a {{ color: #45abff; }}
# # # # #             .dark-theme .post-header {{ color: #b0b3b8; }}
# # # # #             .dark-theme .post-header .post-id {{ color: #ff6347; font-weight: bold; }}
# # # # #             .dark-theme .theme-toggle-button {{ background-color: #eee; color: #111; }}
# # # # #         </style>
# # # # #     </head>
# # # # #     <body class="{initial_theme}-theme">
# # # # #         <button id="theme-toggle" class="theme-toggle-button">Cambiar Tema</button>
# # # # #         <div class="container">
# # # # #             <h1><a href="https://boards.4chan.org/{board_name}/thread/{thread_id}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
# # # # #     """
# # # # #     for post in thread.all_posts:
# # # # #         html_content += f"""
# # # # #             <div class="post">
# # # # #                 <div class="post-header"><span class="post-id">Anónimo No.{post.post_id}</span> - <span>{datetime.fromtimestamp(post.timestamp)}</span></div>
# # # # #                 <div class="post-comment">
# # # # #         """
# # # # #         if post.has_file:
# # # # #             image_name = post.file_url.split('/')[-1]
# # # # #             html_content += f'<a href="images/{image_name}" target="_blank"><img src="images/{image_name}" alt="{image_name}"></a>'
# # # # #         comment_html = post.comment.replace('\n', '<br>')
# # # # #         html_content += comment_html
# # # # #         html_content += "</div></div>"
# # # # #     html_content += """
# # # # #         </div>
# # # # #         <script>
# # # # #             const themeToggle = document.getElementById('theme-toggle');
# # # # #             const body = document.body;
# # # # #             const applyTheme = (theme) => {
# # # # #                 body.className = theme + '-theme';
# # # # #                 themeToggle.textContent = theme === 'light' ? '🌙 Modo Noche' : '☀️ Modo Día';
# # # # #                 localStorage.setItem('theme', theme);
# # # # #             };
# # # # #             themeToggle.addEventListener('click', () => {
# # # # #                 const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light';
# # # # #                 applyTheme(newTheme);
# # # # #             });
# # # # #             const savedTheme = localStorage.getItem('theme') || '""" + initial_theme + """';
# # # # #             applyTheme(savedTheme);
# # # # #         </script>
# # # # #     </body></html>
# # # # #     """
# # # # #     return html_content

# # # # # def download_thread(board_name, thread_id, theme='light', overwrite=False):
# # # # #     """
# # # # #     NUEVO: Descarga o actualiza un hilo.
# # # # #     Si el hilo ya existe, solo descarga los archivos nuevos.
# # # # #     Si se usa `overwrite=True`, vuelve a descargar todo.
# # # # #     """
# # # # #     try:
# # # # #         board = basc_py4chan.Board(board_name)
# # # # #         thread = board.get_thread(thread_id)
# # # # #         if not thread:
# # # # #             # Silenciado para no ensuciar la salida de la barra de progreso
# # # # #             return thread_id 

# # # # #         thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
# # # # #         sanitized_subject = sanitize_filename(thread_subject)
        
# # # # #         folder_name = f"{thread_id}_{sanitized_subject}"
# # # # #         thread_folder = os.path.join("4chan_downloader", board_name, folder_name)
# # # # #         images_folder = os.path.join(thread_folder, "images")

# # # # #         is_update = os.path.exists(thread_folder)
        
# # # # #         # Crear carpetas si no existen
# # # # #         if not is_update:
# # # # #             os.makedirs(images_folder)

# # # # #         # Descargar archivos
# # # # #         new_files_downloaded = 0
# # # # #         for post in thread.all_posts:
# # # # #             if post.has_file:
# # # # #                 image_name = post.file_url.split('/')[-1]
# # # # #                 image_path = os.path.join(images_folder, image_name)
                
# # # # #                 # La lógica clave: si no es overwrite Y el archivo ya existe, saltárselo.
# # # # #                 if not overwrite and os.path.exists(image_path):
# # # # #                     continue
                
# # # # #                 if download_file(post.file_url, images_folder):
# # # # #                     new_files_downloaded += 1
        
# # # # #         # Siempre se regenera el HTML para asegurar que está actualizado con los últimos posts.
# # # # #         html_content = create_thread_html(thread, board_name, thread_id, thread_subject, theme)
# # # # #         html_filename = f"{thread_id}_{sanitized_subject}.html"
# # # # #         with open(os.path.join(thread_folder, html_filename), "w", encoding="utf-8") as f:
# # # # #             f.write(html_content)

# # # # #         # Devolver datos para el reporte final en la barra de progreso
# # # # #         return {
# # # # #             "id": thread_id,
# # # # #             "subject": thread_subject,
# # # # #             "status": "updated" if is_update else "downloaded",
# # # # #             "new_files": new_files_downloaded
# # # # #         }

# # # # #     except Exception:
# # # # #         return None # Indica un error en este hilo

# # # # # def download_board(board_name, theme='light', overwrite=False):
# # # # #     """Descarga o actualiza todos los hilos de un foro de forma concurrente."""
# # # # #     try:
# # # # #         board = basc_py4chan.Board(board_name)
# # # # #         all_thread_ids = board.get_all_thread_ids()
# # # # #     except Exception as e:
# # # # #         print(f"Error: No se pudo obtener la lista de hilos de /{board_name}/: {e}")
# # # # #         return

# # # # #     max_workers = min(10, os.cpu_count() + 4 if os.cpu_count() else 5)
    
# # # # #     print(f"Iniciando descarga/actualización de {len(all_thread_ids)} hilos de /{board_name}/...")

# # # # #     with ThreadPoolExecutor(max_workers=max_workers) as executor:
# # # # #         args = [(board_name, thread_id, theme, overwrite) for thread_id in all_thread_ids]
        
# # # # #         results = list(tqdm(executor.map(lambda p: download_thread(*p), args), 
# # # # #                             total=len(all_thread_ids), 
# # # # #                             desc=f"Procesando /{board_name}/"))

# # # # #     print(f"\nProceso del foro /{board_name}/ completado.")


# # # # # def main():
# # # # #     """Función principal con argparse para un manejo robusto de argumentos."""
# # # # #     parser = argparse.ArgumentParser(
# # # # #         description="Descarga o actualiza hilos/foros de 4chan para verlos offline.",
# # # # #         formatter_class=argparse.RawTextHelpFormatter,
# # # # #         epilog="""Ejemplos de uso:
# # # # #   # Descargar o actualizar un solo hilo
# # # # #   python %(prog)s https://boards.4chan.org/wg/thread/1234567

# # # # #   # Descargar o actualizar un foro completo con tema oscuro
# # # # #   python %(prog)s https://boards.4chan.org/g/ --tema dark
  
# # # # #   # Forzar la re-descarga de todas las imágenes de un hilo
# # # # #   python %(prog)s https://boards.4chan.org/wg/thread/1234567 --overwrite
# # # # # """
# # # # #     )
# # # # #     parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
# # # # #     parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', 
# # # # #                         help="Elige el tema inicial para los archivos HTML. Default: light.")
# # # # #     # NUEVO ARGUMENTO
# # # # #     parser.add_argument("--overwrite", action="store_true",
# # # # #                         help="Fuerza la descarga de todos los archivos de imagen, incluso si ya existen.")
    
# # # # #     args = parser.parse_args()
    
# # # # #     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
# # # # #     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)

# # # # #     if thread_match:
# # # # #         board_name = thread_match.group(1)
# # # # #         thread_id = int(thread_match.group(2))
        
# # # # #         # Determinar si es una actualización para el mensaje inicial
# # # # #         is_update_check = os.path.exists(os.path.join("4chan_downloader", board_name, f"{thread_id}_"))
# # # # #         action_word = "Actualizando" if is_update_check and not args.overwrite else "Descargando"
# # # # #         print(f"{action_word} el hilo {thread_id} de /{board_name}/...")

# # # # #         result = download_thread(board_name, thread_id, args.tema, args.overwrite)
        
# # # # #         if result:
# # # # #             status_text = "actualizado" if result['status'] == 'updated' else "descargado"
# # # # #             print(f"Hilo '{result['subject']}' {status_text} con éxito. Se añadieron {result['new_files']} archivos nuevos.")
# # # # #         else:
# # # # #             print("No se pudo procesar el hilo.")

# # # # #     elif board_match:
# # # # #         board_name = board_match.group(1)
# # # # #         download_board(board_name, args.tema, args.overwrite)
# # # # #     else:
# # # # #         print("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# # # # # if __name__ == "__main__":
# # # # #     main()


# # # # # v5.1 funciona, pero da problemas para descargar porque 4chan bloquea muchas descargas
# # # # import basc_py4chan
# # # # import requests
# # # # import os
# # # # import sys # NUEVO: Para imprimir errores en la salida de error estándar
# # # # import re
# # # # import argparse
# # # # from datetime import datetime
# # # # from concurrent.futures import ThreadPoolExecutor
# # # # from tqdm import tqdm

# # # # def sanitize_filename(name):
# # # #     """Limpia un string para que sea un nombre de archivo/carpeta válido."""
# # # #     sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
# # # #     sanitized_name = sanitized_name.replace(" ", "_")
# # # #     return sanitized_name[:100]

# # # # def download_file(url, folder):
# # # #     """
# # # #     Descarga un archivo.
# # # #     MODIFICADO: Timeout aumentado y reporte de errores visible.
# # # #     """
# # # #     try:
# # # #         # Aumentado el timeout a 60 segundos para archivos grandes como webm
# # # #         response = requests.get(url, stream=True, timeout=60)
# # # #         response.raise_for_status()
# # # #         filename = os.path.join(folder, url.split('/')[-1])
# # # #         with open(filename, 'wb') as f:
# # # #             for chunk in response.iter_content(chunk_size=8192):
# # # #                 f.write(chunk)
# # # #         return filename
# # # #     except requests.exceptions.RequestException as e:
# # # #         # Imprimir errores en lugar de fallar silenciosamente.
# # # #         # El \n inicial asegura que el mensaje no interfiera con la barra de tqdm.
# # # #         print(f"\n[ERROR] No se pudo descargar el archivo {url}. Razón: {e}", file=sys.stderr)
# # # #         return None

# # # # def create_thread_html(thread, board_name, thread_id, thread_subject, initial_theme='light'):
# # # #     """Crea un archivo HTML que diferencia entre imágenes y videos (webm/mp4). (Sin cambios)"""
# # # #     html_content = f"""
# # # #     <!DOCTYPE html>
# # # #     <html lang="es">
# # # #     <head>
# # # #         <meta charset="UTF-8">
# # # #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # #         <title>{board_name} - {thread_subject} ({thread_id})</title>
# # # #         <style>
# # # #             body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 1em; line-height: 1.6; transition: background-color 0.3s, color 0.3s; }}
# # # #             .container {{ max-width: 800px; margin: 0 auto; padding: 1em; }}
# # # #             a {{ text-decoration: none; }}
# # # #             a:hover {{ text-decoration: underline; }}
# # # #             img, video {{ max-width: 350px; max-height: 400px; height: auto; cursor: pointer; border-radius: 4px; display: block; margin-bottom: 1em; }}
# # # #             .post {{ margin-bottom: 1.5em; padding: 1em; border-radius: 8px; transition: background-color 0.3s, border-color 0.3s; }}
# # # #             .post-header {{ font-size: 0.9em; margin-bottom: 0.5em; }}
# # # #             .post-comment {{ word-wrap: break-word; }}
# # # #             .theme-toggle-button {{ position: fixed; top: 15px; right: 15px; padding: 8px 12px; border-radius: 20px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s, color 0.3s; }}
# # # #             body.light-theme {{ background-color: #f0f2f5; color: #1c1e21; }}
# # # #             .light-theme .post {{ background-color: #ffffff; border: 1px solid #dddfe2; }}
# # # #             .light-theme a {{ color: #0d86ff; }}
# # # #             .light-theme .post-header {{ color: #606770; }}
# # # #             .light-theme .post-header .post-id {{ color: #d00; font-weight: bold; }}
# # # #             .light-theme .theme-toggle-button {{ background-color: #333; color: #fff; }}
# # # #             body.dark-theme {{ background-color: #18191a; color: #e4e6eb; }}
# # # #             .dark-theme .post {{ background-color: #242526; border: 1px solid #3a3b3c; }}
# # # #             .dark-theme a {{ color: #45abff; }}
# # # #             .dark-theme .post-header {{ color: #b0b3b8; }}
# # # #             .dark-theme .post-header .post-id {{ color: #ff6347; font-weight: bold; }}
# # # #             .dark-theme .theme-toggle-button {{ background-color: #eee; color: #111; }}
# # # #         </style>
# # # #     </head>
# # # #     <body class="{initial_theme}-theme">
# # # #         <button id="theme-toggle" class="theme-toggle-button">Cambiar Tema</button>
# # # #         <div class="container">
# # # #             <h1><a href="https://boards.4chan.org/{board_name}/thread/{thread_id}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
# # # #     """
# # # #     for post in thread.all_posts:
# # # #         html_content += f"""
# # # #             <div class="post">
# # # #                 <div class="post-header"><span class="post-id">Anónimo No.{post.post_id}</span> - <span>{datetime.fromtimestamp(post.timestamp)}</span></div>
# # # #                 <div class="post-comment">
# # # #         """
# # # #         if post.has_file:
# # # #             file_name = post.file_url.split('/')[-1]
# # # #             file_path_relative = f"images/{file_name}"
# # # #             file_extension = os.path.splitext(file_name)[1].lower()
# # # #             if file_extension in ['.webm', '.mp4']:
# # # #                 html_content += f"""
# # # #                     <video controls muted loop preload="metadata">
# # # #                         <source src="{file_path_relative}" type="video/{file_extension[1:]}">
# # # #                         Tu navegador no soporta la etiqueta de video. <a href="{file_path_relative}">Descargar video</a>
# # # #                     </video>
# # # #                 """
# # # #             elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
# # # #                 html_content += f'<a href="{file_path_relative}" target="_blank"><img src="{file_path_relative}" alt="{file_name}"></a>'
# # # #             else:
# # # #                 html_content += f'<p>Archivo adjunto: <a href="{file_path_relative}" target="_blank">{file_name}</a></p>'
# # # #         comment_html = post.comment.replace('\n', '<br>')
# # # #         html_content += comment_html
# # # #         html_content += "</div></div>"
# # # #     html_content += """
# # # #         </div>
# # # #         <script>
# # # #             const themeToggle = document.getElementById('theme-toggle');
# # # #             const body = document.body;
# # # #             const applyTheme = (theme) => {
# # # #                 body.className = theme + '-theme';
# # # #                 themeToggle.textContent = theme === 'light' ? '🌙 Modo Noche' : '☀️ Modo Día';
# # # #                 localStorage.setItem('theme', theme);
# # # #             };
# # # #             themeToggle.addEventListener('click', () => {
# # # #                 const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light';
# # # #                 applyTheme(newTheme);
# # # #             });
# # # #             const savedTheme = localStorage.getItem('theme') || '""" + initial_theme + """';
# # # #             applyTheme(savedTheme);
# # # #         </script>
# # # #     </body></html>
# # # #     """
# # # #     return html_content

# # # # def download_thread(board_name, thread_id, theme='light', overwrite=False):
# # # #     """Descarga o actualiza un hilo, manejando eficientemente los archivos existentes."""
# # # #     try:
# # # #         board = basc_py4chan.Board(board_name)
# # # #         thread = board.get_thread(thread_id)
# # # #         if not thread: return None

# # # #         thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
# # # #         sanitized_subject = sanitize_filename(thread_subject)
        
# # # #         folder_name = f"{thread_id}_{sanitized_subject}"
# # # #         thread_folder = os.path.join("4chan_downloader", board_name, folder_name)
# # # #         images_folder = os.path.join(thread_folder, "images")

# # # #         is_update = os.path.exists(thread_folder)
# # # #         if not is_update: os.makedirs(images_folder)

# # # #         new_files_downloaded = 0
# # # #         for post in thread.all_posts:
# # # #             if post.has_file:
# # # #                 image_name = post.file_url.split('/')[-1]
# # # #                 image_path = os.path.join(images_folder, image_name)
                
# # # #                 if not overwrite and os.path.exists(image_path): continue
                
# # # #                 if download_file(post.file_url, images_folder):
# # # #                     new_files_downloaded += 1
        
# # # #         html_content = create_thread_html(thread, board_name, thread_id, thread_subject, theme)
# # # #         html_filename = f"{thread_id}_{sanitized_subject}.html"
# # # #         with open(os.path.join(thread_folder, html_filename), "w", encoding="utf-8") as f:
# # # #             f.write(html_content)

# # # #         return {"id": thread_id, "subject": thread_subject, "status": "updated" if is_update else "downloaded", "new_files": new_files_downloaded}
# # # #     except Exception as e:
# # # #         print(f"\n[ERROR] No se pudo procesar el hilo {thread_id}. Razón: {e}", file=sys.stderr)
# # # #         return None

# # # # def download_board(board_name, theme='light', overwrite=False):
# # # #     """
# # # #     Descarga o actualiza todos los hilos de un foro.
# # # #     MODIFICADO: Añade un resumen final.
# # # #     """
# # # #     try:
# # # #         board = basc_py4chan.Board(board_name)
# # # #         all_thread_ids = board.get_all_thread_ids()
# # # #     except Exception as e:
# # # #         print(f"Error: No se pudo obtener la lista de hilos de /{board_name}/: {e}")
# # # #         return

# # # #     max_workers = min(10, os.cpu_count() + 4 if os.cpu_count() else 5)
# # # #     print(f"Iniciando descarga/actualización de {len(all_thread_ids)} hilos de /{board_name}/...")
    
# # # #     results = []
# # # #     with ThreadPoolExecutor(max_workers=max_workers) as executor:
# # # #         args = [(board_name, thread_id, theme, overwrite) for thread_id in all_thread_ids]
# # # #         results = list(tqdm(executor.map(lambda p: download_thread(*p), args), total=len(all_thread_ids), desc=f"Procesando /{board_name}/"))

# # # #     success_count = sum(1 for r in results if r is not None)
# # # #     fail_count = len(results) - success_count
    
# # # #     print("\n----- RESUMEN DEL PROCESO -----")
# # # #     print(f"Proceso del foro /{board_name}/ completado.")
# # # #     print(f"Hilos exitosos: {success_count}")
# # # #     print(f"Hilos fallidos: {fail_count}")
# # # #     print("-----------------------------")

# # # # def main():
# # # #     """Función principal con argparse."""
# # # #     parser = argparse.ArgumentParser(
# # # #         description="Descarga o actualiza hilos/foros de 4chan para verlos offline. v5.1 con descarga de video corregida.",
# # # #         formatter_class=argparse.RawTextHelpFormatter,
# # # #         epilog="""Ejemplos de uso:
# # # #   # Descargar o actualizar un solo hilo
# # # #   python %(prog)s https://boards.4chan.org/wsg/thread/5891302

# # # #   # Descargar o actualizar un foro completo con tema oscuro
# # # #   python %(prog)s https://boards.4chan.org/wsg/ --tema dark
  
# # # #   # Forzar la re-descarga de todos los archivos de un hilo
# # # #   python %(prog)s https://boards.4chan.org/wsg/thread/5891302 --overwrite
# # # # """)
# # # #     parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
# # # #     parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', help="Elige el tema inicial para los archivos HTML. Default: light.")
# # # #     parser.add_argument("--overwrite", action="store_true", help="Fuerza la descarga de todos los archivos, incluso si ya existen.")
    
# # # #     args = parser.parse_args()
    
# # # #     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
# # # #     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)

# # # #     if thread_match:
# # # #         board_name, thread_id = thread_match.groups()
# # # #         thread_id = int(thread_id)
        
# # # #         # Esta comprobación es imperfecta para el nombre, pero sirve para el mensaje
# # # #         base_path = os.path.join("4chan_downloader", board_name)
# # # #         is_update_check = False
# # # #         if os.path.exists(base_path):
# # # #             is_update_check = any(os.path.isdir(os.path.join(base_path, d)) for d in os.listdir(base_path) if d.startswith(str(thread_id)))

# # # #         action_word = "Actualizando" if is_update_check and not args.overwrite else "Descargando"
# # # #         print(f"{action_word} el hilo {thread_id} de /{board_name}/...")

# # # #         result = download_thread(board_name, thread_id, args.tema, args.overwrite)
        
# # # #         if result:
# # # #             status_text = "actualizado" if result['status'] == 'updated' else "descargado"
# # # #             print(f"Hilo '{result['subject']}' {status_text} con éxito. Se añadieron {result['new_files']} archivos nuevos.")
# # # #         else:
# # # #             print(f"La operación del hilo {thread_id} falló. Revisa los mensajes de error de arriba.")

# # # #     elif board_match:
# # # #         board_name = board_match.group(1)
# # # #         download_board(board_name, args.tema, args.overwrite)
# # # #     else:
# # # #         print("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# # # # if __name__ == "__main__":
# # # #     main()


# # # # v6.0 funciona
# # # import basc_py4chan
# # # import requests
# # # import os
# # # import sys
# # # import re
# # # import argparse
# # # from datetime import datetime
# # # from concurrent.futures import ThreadPoolExecutor
# # # from tqdm import tqdm

# # # def sanitize_filename(name):
# # #     """Limpia un string para que sea un nombre de archivo/carpeta válido."""
# # #     sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
# # #     sanitized_name = sanitized_name.replace(" ", "_")
# # #     return sanitized_name[:100]

# # # def download_file(url, folder):
# # #     """Descarga un archivo. Con timeout largo y reporte de errores visible."""
# # #     try:
# # #         response = requests.get(url, stream=True, timeout=60)
# # #         response.raise_for_status()
# # #         filename = os.path.join(folder, url.split('/')[-1])
# # #         with open(filename, 'wb') as f:
# # #             for chunk in response.iter_content(chunk_size=8192):
# # #                 f.write(chunk)
# # #         return filename
# # #     except requests.exceptions.RequestException as e:
# # #         print(f"\n[ERROR] No se pudo descargar el archivo {url}. Razón: {e}", file=sys.stderr)
# # #         return None

# # # def create_thread_html(thread, board_name, thread_id, thread_subject, initial_theme='light'):
# # #     """Crea un archivo HTML que diferencia entre imágenes y videos (webm/mp4)."""
# # #     # (Sin cambios respecto a la v5.1)
# # #     html_content = f"""
# # #     <!DOCTYPE html>
# # #     <html lang="es">
# # #     <head>
# # #         <meta charset="UTF-8">
# # #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # #         <title>{board_name} - {thread_subject} ({thread_id})</title>
# # #         <style>
# # #             body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 1em; line-height: 1.6; transition: background-color 0.3s, color 0.3s; }}
# # #             .container {{ max-width: 800px; margin: 0 auto; padding: 1em; }}
# # #             a {{ text-decoration: none; }}
# # #             a:hover {{ text-decoration: underline; }}
# # #             img, video {{ max-width: 350px; max-height: 400px; height: auto; cursor: pointer; border-radius: 4px; display: block; margin-bottom: 1em; }}
# # #             .post {{ margin-bottom: 1.5em; padding: 1em; border-radius: 8px; transition: background-color 0.3s, border-color 0.3s; }}
# # #             .post-header {{ font-size: 0.9em; margin-bottom: 0.5em; }}
# # #             .post-comment {{ word-wrap: break-word; }}
# # #             .theme-toggle-button {{ position: fixed; top: 15px; right: 15px; padding: 8px 12px; border-radius: 20px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s, color 0.3s; }}
# # #             body.light-theme {{ background-color: #f0f2f5; color: #1c1e21; }}
# # #             .light-theme .post {{ background-color: #ffffff; border: 1px solid #dddfe2; }}
# # #             .light-theme a {{ color: #0d86ff; }}
# # #             .light-theme .post-header {{ color: #606770; }}
# # #             .light-theme .post-header .post-id {{ color: #d00; font-weight: bold; }}
# # #             .light-theme .theme-toggle-button {{ background-color: #333; color: #fff; }}
# # #             body.dark-theme {{ background-color: #18191a; color: #e4e6eb; }}
# # #             .dark-theme .post {{ background-color: #242526; border: 1px solid #3a3b3c; }}
# # #             .dark-theme a {{ color: #45abff; }}
# # #             .dark-theme .post-header {{ color: #b0b3b8; }}
# # #             .dark-theme .post-header .post-id {{ color: #ff6347; font-weight: bold; }}
# # #             .dark-theme .theme-toggle-button {{ background-color: #eee; color: #111; }}
# # #         </style>
# # #     </head>
# # #     <body class="{initial_theme}-theme">
# # #         <button id="theme-toggle" class="theme-toggle-button">Cambiar Tema</button>
# # #         <div class="container">
# # #             <h1><a href="https://boards.4chan.org/{board_name}/thread/{thread_id}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
# # #     """
# # #     for post in thread.all_posts:
# # #         html_content += f"""
# # #             <div class="post">
# # #                 <div class="post-header"><span class="post-id">Anónimo No.{post.post_id}</span> - <span>{datetime.fromtimestamp(post.timestamp)}</span></div>
# # #                 <div class="post-comment">
# # #         """
# # #         if post.has_file:
# # #             file_name = post.file_url.split('/')[-1]
# # #             file_path_relative = f"images/{file_name}"
# # #             file_extension = os.path.splitext(file_name)[1].lower()
# # #             if file_extension in ['.webm', '.mp4']:
# # #                 html_content += f"""
# # #                     <video controls muted loop preload="metadata">
# # #                         <source src="{file_path_relative}" type="video/{file_extension[1:]}">
# # #                         Tu navegador no soporta la etiqueta de video. <a href="{file_path_relative}">Descargar video</a>
# # #                     </video>
# # #                 """
# # #             elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
# # #                 html_content += f'<a href="{file_path_relative}" target="_blank"><img src="{file_path_relative}" alt="{file_name}"></a>'
# # #             else:
# # #                 html_content += f'<p>Archivo adjunto: <a href="{file_path_relative}" target="_blank">{file_name}</a></p>'
# # #         comment_html = post.comment.replace('\n', '<br>')
# # #         html_content += comment_html
# # #         html_content += "</div></div>"
# # #     html_content += """
# # #         </div>
# # #         <script>
# # #             const themeToggle = document.getElementById('theme-toggle');
# # #             const body = document.body;
# # #             const applyTheme = (theme) => {
# # #                 body.className = theme + '-theme';
# # #                 themeToggle.textContent = theme === 'light' ? '🌙 Modo Noche' : '☀️ Modo Día';
# # #                 localStorage.setItem('theme', theme);
# # #             };
# # #             themeToggle.addEventListener('click', () => {
# # #                 const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light';
# # #                 applyTheme(newTheme);
# # #             });
# # #             const savedTheme = localStorage.getItem('theme') || '""" + initial_theme + """';
# # #             applyTheme(savedTheme);
# # #         </script>
# # #     </body></html>
# # #     """
# # #     return html_content

# # # def download_thread(board_name, thread_id, theme='light', overwrite=False):
# # #     """Descarga o actualiza un hilo, manejando eficientemente los archivos existentes."""
# # #     try:
# # #         board = basc_py4chan.Board(board_name)
# # #         thread = board.get_thread(thread_id)
# # #         if not thread: return None

# # #         thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
# # #         sanitized_subject = sanitize_filename(thread_subject)
        
# # #         folder_name = f"{thread_id}_{sanitized_subject}"
# # #         thread_folder = os.path.join("4chan_downloader", board_name, folder_name)
# # #         images_folder = os.path.join(thread_folder, "images")

# # #         is_update = os.path.exists(thread_folder)
# # #         if not is_update: os.makedirs(images_folder)

# # #         new_files_downloaded = 0
# # #         for post in thread.all_posts:
# # #             if post.has_file:
# # #                 image_name = post.file_url.split('/')[-1]
# # #                 image_path = os.path.join(images_folder, image_name)
                
# # #                 if not overwrite and os.path.exists(image_path): continue
                
# # #                 if download_file(post.file_url, images_folder):
# # #                     new_files_downloaded += 1
        
# # #         html_content = create_thread_html(thread, board_name, thread_id, thread_subject, theme)
# # #         html_filename = f"{thread_id}_{sanitized_subject}.html"
# # #         with open(os.path.join(thread_folder, html_filename), "w", encoding="utf-8") as f:
# # #             f.write(html_content)

# # #         return {"id": thread_id, "subject": thread_subject, "status": "updated" if is_update else "downloaded", "new_files": new_files_downloaded}
# # #     except Exception as e:
# # #         print(f"\n[ERROR] No se pudo procesar el hilo {thread_id}. Razón: {e}", file=sys.stderr)
# # #         return None

# # # def download_board(board_name, theme='light', overwrite=False, multithread=False):
# # #     """
# # #     MODIFICADO: Descarga hilos de forma secuencial por defecto, o en paralelo
# # #     si multithread es True.
# # #     """
# # #     try:
# # #         board = basc_py4chan.Board(board_name)
# # #         all_thread_ids = board.get_all_thread_ids()
# # #     except Exception as e:
# # #         print(f"Error: No se pudo obtener la lista de hilos de /{board_name}/: {e}")
# # #         return

# # #     results = []
# # #     if multithread:
# # #         # Modo multi-hilo (rápido pero riesgoso)
# # #         # Número de workers reducido a 5 para ser más amable con la API.
# # #         max_workers = 5
# # #         print(f"Iniciando descarga en modo MULTI-HILO ({max_workers} hilos) para {len(all_thread_ids)} posts...")
# # #         with ThreadPoolExecutor(max_workers=max_workers) as executor:
# # #             args = [(board_name, thread_id, theme, overwrite) for thread_id in all_thread_ids]
# # #             results = list(tqdm(executor.map(lambda p: download_thread(*p), args), total=len(all_thread_ids), desc=f"Procesando /{board_name}/ (Multi-hilo)"))
# # #     else:
# # #         # Modo secuencial (lento pero seguro, por defecto)
# # #         print(f"Iniciando descarga en modo SECUENCIAL para {len(all_thread_ids)} hilos...")
# # #         for thread_id in tqdm(all_thread_ids, desc=f"Procesando /{board_name}/ (Secuencial)"):
# # #             result = download_thread(board_name, thread_id, theme, overwrite)
# # #             results.append(result)

# # #     success_count = sum(1 for r in results if r is not None)
# # #     fail_count = len(results) - success_count
    
# # #     print("\n----- RESUMEN DEL PROCESO -----")
# # #     print(f"Proceso del foro /{board_name}/ completado.")
# # #     print(f"Hilos exitosos: {success_count}")
# # #     print(f"Hilos fallidos: {fail_count}")
# # #     print("-----------------------------")

# # # def main():
# # #     """Función principal con argparse."""
# # #     parser = argparse.ArgumentParser(
# # #         description="Descarga o actualiza hilos/foros de 4chan para verlos offline. v6.0",
# # #         formatter_class=argparse.RawTextHelpFormatter,
# # #         epilog="""Ejemplos de uso:
# # #   # Descarga segura (secuencial) de un foro (RECOMENDADO)
# # #   python %(prog)s https://boards.4chan.org/x/

# # #   # Descarga RÁPIDA (multi-hilo) de un foro (puede causar errores '429')
# # #   python %(prog)s https://boards.4chan.org/x/ -mt

# # #   # Descargar un solo hilo (siempre es secuencial)
# # #   python %(prog)s https://boards.4chan.org/x/thread/123456
  
# # #   # Forzar la re-descarga de todos los archivos de un hilo
# # #   python %(prog)s https://boards.4chan.org/x/thread/123456 --overwrite
# # # """)
# # #     parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
# # #     parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', help="Elige el tema inicial para los archivos HTML. Default: light.")
# # #     parser.add_argument("--overwrite", action="store_true", help="Fuerza la descarga de todos los archivos, incluso si ya existen.")
# # #     # NUEVO ARGUMENTO
# # #     parser.add_argument("-mt", "--multithread", action="store_true",
# # #                         help="Activa la descarga multi-hilo para foros. Es más rápido pero puede causar errores '429 Too Many Requests'. Por defecto es secuencial y seguro.")
    
# # #     args = parser.parse_args()
    
# # #     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
# # #     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)

# # #     if thread_match:
# # #         board_name, thread_id = thread_match.groups()
# # #         thread_id = int(thread_id)
        
# # #         base_path = os.path.join("4chan_downloader", board_name)
# # #         is_update_check = False
# # #         if os.path.exists(base_path):
# # #             try:
# # #                 is_update_check = any(os.path.isdir(os.path.join(base_path, d)) for d in os.listdir(base_path) if d.startswith(str(thread_id)))
# # #             except FileNotFoundError:
# # #                 is_update_check = False

# # #         action_word = "Actualizando" if is_update_check and not args.overwrite else "Descargando"
# # #         print(f"{action_word} el hilo {thread_id} de /{board_name}/...")

# # #         result = download_thread(board_name, thread_id, args.tema, args.overwrite)
        
# # #         if result:
# # #             status_text = "actualizado" if result['status'] == 'updated' else "descargado"
# # #             print(f"Hilo '{result['subject']}' {status_text} con éxito. Se añadieron {result['new_files']} archivos nuevos.")
# # #         else:
# # #             print(f"La operación del hilo {thread_id} falló. Revisa los mensajes de error de arriba.")

# # #     elif board_match:
# # #         board_name = board_match.group(1)
# # #         # Pasamos el nuevo argumento a la función
# # #         download_board(board_name, args.tema, args.overwrite, args.multithread)
# # #     else:
# # #         print("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# # # if __name__ == "__main__":
# # #     main()

# # version 7: reintentos y sleep

# import basc_py4chan
# import requests
# import os
# import sys
# import re
# import argparse
# import time # NUEVO: Para las pausas y reintentos
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor
# from tqdm import tqdm

# def sanitize_filename(name):
#     """Limpia un string para que sea un nombre de archivo/carpeta válido."""
#     sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
#     sanitized_name = sanitized_name.replace(" ", "_")
#     return sanitized_name[:100]

# def download_file(url, folder, retries=3):
#     """
#     MODIFICADO: Descarga un archivo con reintentos y exponential backoff.
#     """
#     backoff_factor = 2  # El tiempo de espera se duplicará en cada reintento
#     for attempt in range(retries):
#         try:
#             response = requests.get(url, stream=True, timeout=60)
#             # Si el código de estado es un error (ej. 4xx, 5xx), lanza una excepción
#             response.raise_for_status()
            
#             filename = os.path.join(folder, url.split('/')[-1])
#             with open(filename, 'wb') as f:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     f.write(chunk)
#             return filename  # Éxito, salimos de la función

#         except requests.exceptions.RequestException as e:
#             # Comprobar si el error es por rate limiting (429) o un error de conexión
#             is_rate_limit = e.response is not None and e.response.status_code == 429
#             is_server_error = e.response is not None and e.response.status_code >= 500
            
#             # Solo reintentamos si es un error de rate limit o un error de servidor/conexión
#             if is_rate_limit or is_server_error or isinstance(e, requests.exceptions.ConnectionError):
#                 if attempt < retries - 1:
#                     wait_time = backoff_factor * (2 ** attempt)
#                     print(f"\n[AVISO] Error al descargar {url}: {e}. Reintentando en {wait_time}s... (Intento {attempt + 1}/{retries})", file=sys.stderr)
#                     time.sleep(wait_time)
#                 else:
#                     print(f"\n[ERROR] Fallaron todos los reintentos para descargar {url}. Razón final: {e}", file=sys.stderr)
#             else:
#                 # Si es otro error de cliente (ej. 404 Not Found), no reintentamos
#                 print(f"\n[ERROR] No se pudo descargar {url} debido a un error irrecuperable: {e}", file=sys.stderr)
#                 break # Salimos del bucle de reintentos
    
#     return None # Si todos los reintentos fallan, devolvemos None

# def create_thread_html(thread, board_name, thread_id, thread_subject, initial_theme='light'):
#     """Crea un archivo HTML que diferencia entre imágenes y videos (webm/mp4). (Sin cambios)"""
#     # Esta función es perfecta como está, no necesita cambios.
#     # ... (código de create_thread_html de la v5.1)
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
#             a {{ text-decoration: none; }}
#             a:hover {{ text-decoration: underline; }}
#             img, video {{ max-width: 350px; max-height: 400px; height: auto; cursor: pointer; border-radius: 4px; display: block; margin-bottom: 1em; }}
#             .post {{ margin-bottom: 1.5em; padding: 1em; border-radius: 8px; transition: background-color 0.3s, border-color 0.3s; }}
#             .post-header {{ font-size: 0.9em; margin-bottom: 0.5em; }}
#             .post-comment {{ word-wrap: break-word; }}
#             .theme-toggle-button {{ position: fixed; top: 15px; right: 15px; padding: 8px 12px; border-radius: 20px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s, color 0.3s; }}
#             body.light-theme {{ background-color: #f0f2f5; color: #1c1e21; }}
#             .light-theme .post {{ background-color: #ffffff; border: 1px solid #dddfe2; }}
#             .light-theme a {{ color: #0d86ff; }}
#             .light-theme .post-header {{ color: #606770; }}
#             .light-theme .post-header .post-id {{ color: #d00; font-weight: bold; }}
#             .light-theme .theme-toggle-button {{ background-color: #333; color: #fff; }}
#             body.dark-theme {{ background-color: #18191a; color: #e4e6eb; }}
#             .dark-theme .post {{ background-color: #242526; border: 1px solid #3a3b3c; }}
#             .dark-theme a {{ color: #45abff; }}
#             .dark-theme .post-header {{ color: #b0b3b8; }}
#             .dark-theme .post-header .post-id {{ color: #ff6347; font-weight: bold; }}
#             .dark-theme .theme-toggle-button {{ background-color: #eee; color: #111; }}
#         </style>
#     </head>
#     <body class="{initial_theme}-theme">
#         <button id="theme-toggle" class="theme-toggle-button">Cambiar Tema</button>
#         <div class="container">
#             <h1><a href="https://boards.4chan.org/{board_name}/thread/{thread_id}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
#     """
#     for post in thread.all_posts:
#         html_content += f"""
#             <div class="post">
#                 <div class="post-header"><span class="post-id">Anónimo No.{post.post_id}</span> - <span>{datetime.fromtimestamp(post.timestamp)}</span></div>
#                 <div class="post-comment">
#         """
#         if post.has_file:
#             file_name = post.file_url.split('/')[-1]
#             file_path_relative = f"images/{file_name}"
#             file_extension = os.path.splitext(file_name)[1].lower()
#             if file_extension in ['.webm', '.mp4']:
#                 html_content += f"""
#                     <video controls muted loop preload="metadata">
#                         <source src="{file_path_relative}" type="video/{file_extension[1:]}">
#                         Tu navegador no soporta la etiqueta de video. <a href="{file_path_relative}">Descargar video</a>
#                     </video>
#                 """
#             elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
#                 html_content += f'<a href="{file_path_relative}" target="_blank"><img src="{file_path_relative}" alt="{file_name}"></a>'
#             else:
#                 html_content += f'<p>Archivo adjunto: <a href="{file_path_relative}" target="_blank">{file_name}</a></p>'
#         comment_html = post.comment.replace('\n', '<br>')
#         html_content += comment_html
#         html_content += "</div></div>"
#     html_content += """
#         </div>
#         <script>
#             const themeToggle = document.getElementById('theme-toggle');
#             const body = document.body;
#             const applyTheme = (theme) => {
#                 body.className = theme + '-theme';
#                 themeToggle.textContent = theme === 'light' ? '🌙 Modo Noche' : '☀️ Modo Día';
#                 localStorage.setItem('theme', theme);
#             };
#             themeToggle.addEventListener('click', () => {
#                 const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light';
#                 applyTheme(newTheme);
#             });
#             const savedTheme = localStorage.getItem('theme') || '""" + initial_theme + """';
#             applyTheme(savedTheme);
#         </script>
#     </body></html>
#     """
#     return html_content

# def download_thread(board_name, thread_id, theme='light', overwrite=False, sleep_time=1, retries=3):
#     """MODIFICADO: Pasa los parámetros de sleep y retries a la función de descarga."""
#     try:
#         board = basc_py4chan.Board(board_name)
#         thread = board.get_thread(thread_id)
#         if not thread: return None

#         thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
#         sanitized_subject = sanitize_filename(thread_subject)
        
#         folder_name = f"{thread_id}_{sanitized_subject}"
#         thread_folder = os.path.join("4chan_downloader", board_name, folder_name)
#         images_folder = os.path.join(thread_folder, "images")

#         is_update = os.path.exists(thread_folder)
#         if not is_update: os.makedirs(images_folder)

#         new_files_downloaded = 0
#         posts_with_files = [post for post in thread.all_posts if post.has_file]

#         for post in posts_with_files:
#             image_name = post.file_url.split('/')[-1]
#             image_path = os.path.join(images_folder, image_name)
            
#             if not overwrite and os.path.exists(image_path): continue
            
#             # Pasamos el número de reintentos a la función de descarga
#             if download_file(post.file_url, images_folder, retries):
#                 new_files_downloaded += 1
            
#             # Hacemos la pausa DESPUÉS de intentar descargar un archivo
#             time.sleep(sleep_time)
        
#         html_content = create_thread_html(thread, board_name, thread_id, thread_subject, theme)
#         html_filename = f"{thread_id}_{sanitized_subject}.html"
#         with open(os.path.join(thread_folder, html_filename), "w", encoding="utf-8") as f:
#             f.write(html_content)

#         return {"id": thread_id, "subject": thread_subject, "status": "updated" if is_update else "downloaded", "new_files": new_files_downloaded}
#     except Exception as e:
#         print(f"\n[ERROR] No se pudo procesar el hilo {thread_id}. Razón: {e}", file=sys.stderr)
#         return None

# def download_board(board_name, theme='light', overwrite=False, multithread=False, sleep_time=1, retries=3):
#     """MODIFICADO: Pasa los parámetros de sleep y retries a download_thread."""
#     try:
#         board = basc_py4chan.Board(board_name)
#         all_thread_ids = board.get_all_thread_ids()
#     except Exception as e:
#         print(f"Error: No se pudo obtener la lista de hilos de /{board_name}/: {e}")
#         return

#     results = []
#     if multithread:
#         max_workers = 5
#         print(f"Iniciando descarga en modo MULTI-HILO ({max_workers} hilos) para {len(all_thread_ids)} posts...")
#         with ThreadPoolExecutor(max_workers=max_workers) as executor:
#             args = [(board_name, thread_id, theme, overwrite, sleep_time, retries) for thread_id in all_thread_ids]
#             results = list(tqdm(executor.map(lambda p: download_thread(*p), args), total=len(all_thread_ids), desc=f"Procesando /{board_name}/ (Multi-hilo)"))
#     else:
#         print(f"Iniciando descarga en modo SECUENCIAL para {len(all_thread_ids)} hilos...")
#         for thread_id in tqdm(all_thread_ids, desc=f"Procesando /{board_name}/ (Secuencial)"):
#             result = download_thread(board_name, thread_id, theme, overwrite, sleep_time, retries)
#             results.append(result)

#     success_count = sum(1 for r in results if r is not None)
#     fail_count = len(results) - success_count
#     print("\n----- RESUMEN DEL PROCESO -----")
#     print(f"Proceso del foro /{board_name}/ completado.")
#     print(f"Hilos exitosos: {success_count}")
#     print(f"Hilos fallidos: {fail_count}")
#     print("-----------------------------")

# def main():
#     """Función principal con argparse."""
#     parser = argparse.ArgumentParser(
#         description="Descarga o actualiza hilos/foros de 4chan para verlos offline. v7.0 con reintentos y pausas.",
#         formatter_class=argparse.RawTextHelpFormatter,
#         epilog="""Ejemplos de uso:
#   # Descarga segura (secuencial, 1s de pausa, 3 reintentos) - RECOMENDADO
#   python %(prog)s https://boards.4chan.org/g/

#   # Descarga más agresiva con una pausa más corta
#   python %(prog)s https://boards.4chan.org/g/ -s 0.5

#   # Descarga RÁPIDA (multi-hilo), pero con pausas en cada hilo para más estabilidad
#   python %(prog)s https://boards.4chan.org/g/ -mt -s 2

#   # Descarga con más reintentos por archivo
#   python %(prog)s https://boards.4chan.org/g/ --retries 5
# """)
#     parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
#     parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', help="Elige el tema inicial para los archivos HTML. (Default: light)")
#     parser.add_argument("--overwrite", action="store_true", help="Fuerza la descarga de todos los archivos, incluso si ya existen.")
#     parser.add_argument("-mt", "--multithread", action="store_true", help="Activa la descarga multi-hilo para foros. Es más rápido pero menos estable. (Default: Secuencial)")
#     # NUEVOS ARGUMENTOS
#     parser.add_argument("-s", "--sleep", type=float, default=1.0, help="Pausa en segundos entre cada descarga de archivo. (Default: 1.0)")
#     parser.add_argument("-r", "--retries", type=int, default=3, help="Número de reintentos por archivo si la descarga falla. (Default: 3)")
    
#     args = parser.parse_args()
    
#     if args.sleep < 0 or args.retries < 0:
#         print("Error: El valor de sleep y retries no puede ser negativo.")
#         return

#     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
#     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)

#     if thread_match:
#         board_name, thread_id = thread_match.groups()
#         thread_id = int(thread_id)
#         print(f"Procesando hilo individual {thread_id} de /{board_name}/...")
#         result = download_thread(board_name, thread_id, args.tema, args.overwrite, args.sleep, args.retries)
#         if result: print(f"Operación completada. Se añadieron {result['new_files']} archivos nuevos.")
#         else: print(f"La operación del hilo {thread_id} falló.")

#     elif board_match:
#         board_name = board_match.group(1)
#         download_board(board_name, args.tema, args.overwrite, args.multithread, args.sleep, args.retries)
#     else:
#         print("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# if __name__ == "__main__":
#     main()


# # #cambio de enfoque, utilizar gallery-dl para descargar imagenes y videos
# # # v8
# # import basc_py4chan
# # import os
# # import sys
# # import re
# # import argparse
# # import subprocess
# # import shutil
# # from datetime import datetime
# # from concurrent.futures import ThreadPoolExecutor
# # from tqdm import tqdm

# # # --- Constantes y Configuración Global ---
# # BASE_DOWNLOAD_DIR = "4chan_downloader"
# # MEDIA_SUBFOLDER = "media" # Nombre de la subcarpeta para imágenes y videos
# # MAX_WORKERS = 5

# # class Console:
# #     """Clase para imprimir mensajes con colores en la consola."""
# #     OKGREEN = '\033[92m'
# #     WARNING = '\033[93m'
# #     FAIL = '\033[91m'
# #     ENDC = '\033[0m'
# #     @staticmethod
# #     def print_success(message): print(f"{Console.OKGREEN}{message}{Console.ENDC}")
# #     @staticmethod
# #     def print_warning(message): print(f"{Console.WARNING}{message}{Console.ENDC}")
# #     @staticmethod
# #     def print_error(message): print(f"{Console.FAIL}{message}{Console.ENDC}", file=sys.stderr)
# #     @staticmethod
# #     def print_info(message): print(message)

# # def check_dependencies():
# #     """Verifica si las dependencias externas (gallery-dl) están instaladas."""
# #     if not shutil.which("gallery-dl"):
# #         Console.print_error("[ERROR CRÍTICO] El comando 'gallery-dl' no fue encontrado.")
# #         Console.print_error("Por favor, asegúrate de que gallery-dl esté instalado: pip install gallery-dl")
# #         sys.exit(1)
# #     Console.print_success("Dependencia 'gallery-dl' encontrada.")

# # def sanitize_filename(name):
# #     """Limpia un string para que sea un nombre de archivo/carpeta válido."""
# #     sanitized_name = re.sub(r'[\\/*?:"<>|]', "", name)
# #     sanitized_name = sanitized_name.replace(" ", "_")
# #     return sanitized_name[:100]

# # def create_thread_html(thread, board_name, thread_id, thread_subject, downloaded_files, initial_theme='light'):
# #     """
# #     Genera el HTML usando basc-py4chan para el texto y una lista de archivos verificados en disco.
# #     Las rutas ahora apuntan a la subcarpeta MEDIA_SUBFOLDER.
# #     """
# #     html_content = f"""
# #     <!DOCTYPE html>
# #     <html lang="es">
# #     <head>
# #         <meta charset="UTF-8">
# #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
# #         <title>{board_name} - {thread_subject} ({thread_id})</title>
# #         <style>
# #             body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 1em; line-height: 1.6; transition: background-color 0.3s, color 0.3s; }}
# #             .container {{ max-width: 800px; margin: 0 auto; padding: 1em; }}
# #             a {{ text-decoration: none; }} a:hover {{ text-decoration: underline; }}
# #             img, video {{ max-width: 350px; max-height: 400px; height: auto; cursor: pointer; border-radius: 4px; display: block; margin-bottom: 1em; }}
# #             .post {{ margin-bottom: 1.5em; padding: 1em; border-radius: 8px; transition: background-color 0.3s, border-color 0.3s; }}
# #             .post-header {{ font-size: 0.9em; margin-bottom: 0.5em; }}
# #             .post-comment {{ word-wrap: break-word; font-size: 1em; line-height: 1.5; }}
# #             .theme-toggle-button {{ position: fixed; top: 15px; right: 15px; padding: 8px 12px; border-radius: 20px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: background-color 0.3s, color 0.3s; }}
# #             footer {{ text-align: center; margin-top: 2em; padding-top: 1em; border-top: 1px solid #ccc; font-size: 0.8em; color: #888; }}
# #             body.light-theme {{ background-color: #f0f2f5; color: #1c1e21; }}
# #             .light-theme .post {{ background-color: #ffffff; border: 1px solid #dddfe2; }} .light-theme a {{ color: #0d86ff; }} .light-theme .post-header {{ color: #606770; }} .light-theme .post-header .post-id {{ color: #d00; font-weight: bold; }} .light-theme .theme-toggle-button {{ background-color: #333; color: #fff; }}
# #             body.dark-theme {{ background-color: #18191a; color: #e4e6eb; }}
# #             .dark-theme .post {{ background-color: #242526; border: 1px solid #3a3b3c; }} .dark-theme a {{ color: #45abff; }} .dark-theme .post-header {{ color: #b0b3b8; }} .dark-theme .post-header .post-id {{ color: #ff6347; font-weight: bold; }} .dark-theme .theme-toggle-button {{ background-color: #eee; color: #111; }} .dark-theme footer {{ border-top-color: #3a3b3c; color: #6d6d6d; }}
# #             .quote {{ color: #789922; }}
# #         </style>
# #     </head>
# #     <body class="{initial_theme}-theme">
# #         <button id="theme-toggle" class="theme-toggle-button">Cambiar Tema</button>
# #         <div class="container">
# #             <h1><a href="{thread.url}" target="_blank">/{board_name}/ - {thread_subject}</a></h1>
# #     """
# #     for post in thread.all_posts:
# #         html_content += f"""
# #             <div class="post">
# #                 <div class="post-header"><span class="post-id">Anónimo No.{post.post_id}</span> - <span>{post.datetime.strftime('%Y-%m-%d %H:%M:%S')}</span></div>
# #                 <div class="post-comment">
# #         """
# #         if post.has_file:
# #             expected_filename = os.path.basename(post.file_url)
# #             if expected_filename in downloaded_files:
# #                 # CORRECCIÓN CLAVE: Se añade la subcarpeta a la ruta del archivo.
# #                 file_path_relative = f"{MEDIA_SUBFOLDER}/{expected_filename}"
# #                 file_extension = os.path.splitext(expected_filename)[1].lower()
# #                 if file_extension in ['.webm', '.mp4']:
# #                     html_content += f"""<video controls muted loop preload="metadata"><source src="{file_path_relative}" type="video/{file_extension[1:]}"></video>"""
# #                 else:
# #                     html_content += f'<a href="{file_path_relative}" target="_blank"><img src="{file_path_relative}" alt="{expected_filename}"></a>'
# #             else:
# #                 html_content += f'<p><i>(Archivo {post.filename} no pudo ser descargado)</i></p>'
        
# #         html_content += post.comment
# #         html_content += "</div></div>"

# #     html_content += f"""
# #         <footer>Generado por 4chan Downloader v14.0 el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</footer>
# #         </div>
# #         <script>
# #             const themeToggle = document.getElementById('theme-toggle'); const body = document.body;
# #             const applyTheme = (theme) => {{ body.className = theme + '-theme'; themeToggle.textContent = theme === 'light' ? '🌙 Modo Noche' : '☀️ Modo Día'; localStorage.setItem('theme', theme); }};
# #             themeToggle.addEventListener('click', () => {{ const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light'; applyTheme(newTheme); }});
# #             const savedTheme = localStorage.getItem('theme') || '{initial_theme}'; applyTheme(savedTheme);
# #         </script>
# #     </body></html>
# #     """
# #     return html_content

# # def download_thread(board_name, thread_id, theme='light', overwrite=False):
# #     """Orquesta la descarga, guardando archivos en una subcarpeta 'media' y verificándolos."""
# #     try:
# #         board = basc_py4chan.Board(board_name)
# #         thread = board.get_thread(thread_id)
# #         if not thread:
# #             Console.print_warning(f"El hilo {thread_id} en /{board_name}/ ya no existe. Saltando.")
# #             return None
        
# #         thread_subject = thread.topic.subject if thread.topic.subject else "Sin_Asunto"
# #         sanitized_subject = sanitize_filename(thread_subject)
        
# #         folder_name = f"{thread_id}_{sanitized_subject}"
# #         thread_folder = os.path.join(BASE_DOWNLOAD_DIR, board_name, folder_name)
# #         # CORRECCIÓN CLAVE: Se define y crea la subcarpeta para los medios.
# #         media_folder = os.path.join(thread_folder, MEDIA_SUBFOLDER)
# #         os.makedirs(media_folder, exist_ok=True)
        
# #         Console.print_info(f"    > Iniciando descarga de medios con gallery-dl en '{media_folder}'...")
        
# #         # CORRECCIÓN CLAVE: Se le dice a gallery-dl que guarde en la subcarpeta
# #         # y que no cree más subcarpetas internas.
# #         command = [
# #             'gallery-dl',
# #             '--directory', media_folder,
# #             '-o', 'path=.', # Evita que gallery-dl cree sub-subcarpetas como '4chan/g/'
# #             thread.url
# #         ]
# #         if overwrite: command.append('--no-skip')

# #         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
# #         for line in iter(process.stdout.readline, ''): print("      " + line, end='')
# #         process.wait()

# #         if process.returncode != 0:
# #             Console.print_warning(f"    > gallery-dl finalizó con errores.")
# #         else:
# #             Console.print_success(f"    > Descarga de medios completada.")

# #         Console.print_info("    > Verificando archivos descargados para construir el HTML...")
# #         try:
# #             # CORRECCIÓN CLAVE: Se verifica el contenido de la subcarpeta de medios.
# #             downloaded_files = set(os.listdir(media_folder))
# #         except FileNotFoundError:
# #             downloaded_files = set()

# #         html_content = create_thread_html(thread, board_name, thread_id, thread_subject, downloaded_files, initial_theme=theme)
# #         html_filename = f"{thread_id}_{sanitized_subject}.html"
# #         with open(os.path.join(thread_folder, html_filename), "w", encoding="utf-8") as f:
# #             f.write(html_content)

# #         return {"id": thread_id, "subject": thread_subject}

# #     except basc_py4chan.exceptions.APIError as e:
# #         if '404' in str(e):
# #              Console.print_warning(f"El hilo https://boards.4chan.org/{board_name}/thread/{thread_id} no fue encontrado (404).")
# #         else:
# #              Console.print_error(f"Error de API de 4chan al procesar el hilo {thread_id}: {e}")
# #         return None
# #     except Exception as e:
# #         Console.print_error(f"Ocurrió un error inesperado al procesar el hilo {thread_id}: {e}")
# #         return None

# # def download_board(board_name, theme='light', overwrite=False, multithread=False):
# #     # Sin cambios en esta función
# #     try:
# #         board = basc_py4chan.Board(board_name)
# #         all_thread_ids = board.get_all_thread_ids()
# #     except Exception as e:
# #         Console.print_error(f"Error: No se pudo obtener la lista de hilos de /{board_name}/: {e}")
# #         return
# #     results = []
# #     if multithread:
# #         Console.print_info(f"Iniciando descarga en modo MULTI-HILO ({MAX_WORKERS} hilos)...")
# #         with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
# #             args = [(board_name, thread_id, theme, overwrite) for thread_id in all_thread_ids]
# #             results = list(tqdm(executor.map(lambda p: download_thread(*p), args), total=len(all_thread_ids), desc=f"Procesando /{board_name}/ (Multi-hilo)"))
# #     else:
# #         Console.print_info(f"Iniciando descarga en modo SECUENCIAL para {len(all_thread_ids)} hilos...")
# #         for thread_id in tqdm(all_thread_ids, desc=f"Procesando /{board_name}/ (Secuencial)"):
# #             results.append(download_thread(board_name, thread_id, theme, overwrite))

# #     success_count = sum(1 for r in results if r is not None)
# #     fail_count = len(results) - success_count
# #     Console.print_info("\n----- RESUMEN DEL PROCESO -----")
# #     Console.print_success(f"Hilos procesados con éxito: {success_count}")
# #     Console.print_warning(f"Hilos fallidos o saltados: {fail_count}")
# #     Console.print_info("-----------------------------")

# # def main():
# #     """Función principal con argparse."""
# #     parser = argparse.ArgumentParser(
# #         description="Descargador de hilos de 4chan. v14.0 - Corrección de rutas y organización.",
# #         formatter_class=argparse.RawTextHelpFormatter)
# #     parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
# #     parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', help="Tema inicial para el HTML.")
# #     parser.add_argument("--overwrite", action="store_true", help="Fuerza la re-verificación de archivos con gallery-dl.")
# #     parser.add_argument("-mt", "--multithread", action="store_true", help="Activa el procesamiento multi-hilo para foros.")
# #     args = parser.parse_args()

# #     check_dependencies()

# #     board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
# #     thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)

# #     if thread_match:
# #         board_name, thread_id = thread_match.groups()
# #         thread_id = int(thread_id)
# #         download_thread(board_name, thread_id, args.tema, args.overwrite)
# #     elif board_match:
# #         board_name = board_match.group(1)
# #         download_board(board_name, args.tema, args.overwrite, args.multithread)
# #     else:
# #         Console.print_error("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

# # if __name__ == "__main__":
# #     main()

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
    for post in thread.all_posts:
        html_content += f"""
            <div class="post">
                <div class="post-header"><span class="post-id">Anónimo No.{post.post_id}</span> - <span>{post.datetime.strftime('%Y-%m-%d %H:%M:%S')}</span></div>
                <div class="post-comment">
        """
        if post.has_file and post.file:
            # CORRECCIÓN: Usar file_extension en lugar de extension
            expected_filename = f"{post.file.filename}{post.file.file_extension}"
            
            if expected_filename in downloaded_files:
                file_path_relative = f"{MEDIA_SUBFOLDER}/{expected_filename}"
                file_extension = os.path.splitext(expected_filename)[1].lower()
                if file_extension in ['.webm', '.mp4']:
                    html_content += f"""<video controls muted loop preload="metadata"><source src="{file_path_relative}" type="video/{file_extension[1:]}"></video>"""
                else:
                    html_content += f'<a href="{file_path_relative}" target="_blank"><img src="{file_path_relative}" alt="{expected_filename}"></a>'
            else:
                html_content += f'<p><i>(Archivo {expected_filename} no pudo ser descargado)</i></p>'
        
        html_content += post.comment
        html_content += "</div></div>"

    html_content += f"""
        <footer>Generado por 4chan Downloader v16.0 el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</footer>
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

def download_thread(board_name, thread_id, theme='light', overwrite=False):
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
            '-o', 'filename={name}',
            thread.url
        ]
        if overwrite: command.append('--no-skip')

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        for line in iter(process.stdout.readline, ''): print("      " + line, end='')
        process.wait()

        if process.returncode != 0:
            Console.print_warning(f"    > gallery-dl finalizó con errores (código: {process.returncode}).")
        else:
            Console.print_success(f"    > Descarga de medios completada.")

        Console.print_info("    > Verificando archivos descargados para construir el HTML...")
        try:
            downloaded_files = set(os.listdir(media_folder))
            Console.print_info(f"    > Archivos encontrados: {len(downloaded_files)}")
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

def download_board(board_name, theme='light', overwrite=False, multithread=False):
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
            args = [(board_name, thread_id, theme, overwrite) for thread_id in all_thread_ids]
            results = list(tqdm(executor.map(lambda p: download_thread(*p), args), total=len(all_thread_ids), desc=f"Procesando /{board_name}/ (Multi-hilo)"))
    else:
        Console.print_info(f"Iniciando descarga en modo SECUENCIAL para {len(all_thread_ids)} hilos...")
        for thread_id in tqdm(all_thread_ids, desc=f"Procesando /{board_name}/ (Secuencial)"):
            results.append(download_thread(board_name, thread_id, theme, overwrite))

    success_count = sum(1 for r in results if r is not None)
    fail_count = len(results) - success_count
    Console.print_info("\n----- RESUMEN DEL PROCESO -----")
    Console.print_success(f"Hilos procesados con éxito: {success_count}")
    Console.print_warning(f"Hilos fallidos o saltados: {fail_count}")
    Console.print_info("-----------------------------")

def main():
    """Función principal con argparse."""
    parser = argparse.ArgumentParser(
        description="Descargador de hilos de 4chan. v16.0 - Corrección final de nombres de archivo.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("url", help="La URL completa del hilo o foro de 4chan.")
    parser.add_argument("-t", "--tema", choices=['light', 'dark'], default='light', help="Tema inicial para el HTML.")
    parser.add_argument("--overwrite", action="store_true", help="Fuerza la re-verificación de archivos con gallery-dl.")
    parser.add_argument("-mt", "--multithread", action="store_true", help="Activa el procesamiento multi-hilo para foros.")
    args = parser.parse_args()

    check_dependencies()

    board_match = re.search(r"boards\.4chan\.org/(\w+)/?$", args.url)
    thread_match = re.search(r"boards\.4chan\.org/(\w+)/thread/(\d+)", args.url)

    if thread_match:
        board_name, thread_id = thread_match.groups()
        thread_id = int(thread_id)
        download_thread(board_name, thread_id, args.tema, args.overwrite)
    elif board_match:
        board_name = board_match.group(1)
        download_board(board_name, args.tema, args.overwrite, args.multithread)
    else:
        Console.print_error("URL no válida. Por favor, introduce una URL de un foro o hilo de 4chan.")

if __name__ == "__main__":
    main()