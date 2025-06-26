# 4chan Downloader v16.2

Un descargador avanzado de hilos y boards de 4chan con interfaz HTML moderna y múltiples opciones de configuración.

## Características

- ✅ Descarga hilos individuales o boards completos
- 🎨 Genera páginas HTML con temas claro/oscuro
- 🖼️ Manejo inteligente de imágenes y videos
- ⚡ Procesamiento paralelo para mayor velocidad
- 📊 Estadísticas detalladas y progreso visual
- 🔧 Sistema de configuración persistente
- 🕒 Control de delay para evitar bans
- 📱 Diseño responsive para móviles
- 📑 Índices navegables para boards completos

## Instalación

### Requisitos

```bash
# Python 3.7+ y pip
pip install basc-py4chan gallery-dl tqdm pathlib
```

### Verificar instalación

```bash
python 4chandlv15.py --config-show
```

## Uso Básico

### Descargar un hilo individual

```bash
# Descarga un hilo específico
python 4chandlv15.py "https://boards.4chan.org/g/thread/12345678"

# Con tema oscuro
python 4chandlv15.py "https://boards.4chan.org/g/thread/12345678" -t dark

# Con delay de 2 segundos entre descargas
python 4chandlv15.py "https://boards.4chan.org/g/thread/12345678" -s 2
```

### Descargar un board completo

```bash
# Descarga todos los hilos de un board
python 4chandlv15.py "https://boards.4chan.org/g/"

# Con procesamiento paralelo (más rápido)
python 4chandlv15.py "https://boards.4chan.org/g/" -mt

# Con delay y paralelo
python 4chandlv15.py "https://boards.4chan.org/g/" -mt -s 1.5
```

## Opciones de Línea de Comandos

### Argumentos Principales

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `url` | URL del hilo o board de 4chan | `"https://boards.4chan.org/g/thread/123"` |
| `-t, --tema` | Tema del HTML (`light`, `dark`) | `-t dark` |
| `-s, --sleep` | Delay en segundos entre descargas | `-s 2.5` |
| `-mt, --multithread` | Activar procesamiento paralelo | `-mt` |
| `--overwrite` | Sobrescribir archivos existentes | `--overwrite` |

### Gestión de Configuración

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--config-show` | Mostrar configuración actual | `--config-show` |
| `--config-set` | Establecer valor de configuración | `--config-set max_workers 10` |

## Configuración Avanzada

### Archivo de Configuración

El script crea automáticamente `4chan_config.json` con la configuración:

```json
{
  "max_workers": 5,
  "default_theme": "light",
  "default_sleep": 0,
  "skip_existing_threads": true,
  "create_index": true
}
```

### Opciones de Configuración

| Parámetro | Tipo | Descripción | Defecto |
|-----------|------|-------------|---------|
| `max_workers` | int | Número de hilos paralelos | `5` |
| `default_theme` | str | Tema por defecto (`light`/`dark`) | `"light"` |
| `default_sleep` | float | Delay por defecto en segundos | `0` |
| `skip_existing_threads` | bool | Saltar hilos ya descargados | `true` |
| `create_index` | bool | Crear índice HTML para boards | `true` |

### Ejemplos de Configuración

```bash
# Cambiar número de workers paralelos
python 4chandlv15.py --config-set max_workers 10

# Establecer tema oscuro por defecto
python 4chandlv15.py --config-set default_theme dark

# Configurar delay por defecto
python 4chandlv15.py --config-set default_sleep 1.5

# Deshabilitar skip de hilos existentes
python 4chandlv15.py --config-set skip_existing_threads false

# Ver configuración actual
python 4chandlv15.py --config-show
```

## Estructura de Archivos

```
4chan_downloader/
├── board_name/
│   ├── index.html                    # Índice del board
│   ├── thread_id_subject/
│   │   ├── thread_id_subject.html    # Página del hilo
│   │   └── media/
│   │       ├── image1.jpg
│   │       ├── video1.webm
│   │       └── ...
│   └── another_thread/
│       └── ...
└── another_board/
    └── ...
```

## Ejemplos de Uso Avanzado

### Descargas Masivas con Control

```bash
# Board completo con máximo control
python 4chandlv15.py "https://boards.4chan.org/g/" \
  -mt \
  -s 2 \
  -t dark \
  --overwrite

# Configurar para descargas masivas
python 4chandlv15.py --config-set max_workers 8
python 4chandlv15.py --config-set default_sleep 1
python 4chandlv15.py "https://boards.4chan.org/wg/" -mt
```

### Workflow Recomendado

1. **Configuración inicial:**
```bash
python 4chandlv15.py --config-set max_workers 3
python 4chandlv15.py --config-set default_sleep 1
```

2. **Descarga de prueba:**
```bash
python 4chandlv15.py "https://boards.4chan.org/g/thread/123456"
```

3. **Descarga de board completo:**
```bash
python 4chandlv15.py "https://boards.4chan.org/g/" -mt
```

## Características del HTML Generado

### Funcionalidades Interactivas

- **Cambio de tema:** Botón para alternar entre claro/oscuro
- **Expansión de imágenes:** Click para ver tamaño completo
- **Videos integrados:** Controles nativos con autoloop
- **Responsive:** Se adapta a pantallas móviles
- **Navegación:** Enlaces a posts y archivos originales

### Información Mostrada

- 📝 Número total de posts
- 🖼️ Cantidad de archivos multimedia
- 💾 Tamaño total de archivos
- 🕒 Fecha y hora de descarga
- 🔗 Enlaces al hilo original

## Solución de Problemas

### Errores Comunes

**Error: "gallery-dl not found"**
```bash
pip install gallery-dl
```

**Error: "Permission denied"**
```bash
# En Linux/Mac, asegurar permisos
chmod +x 4chandlv15.py
```

**Timeout en descargas**
```bash
# Aumentar delay para evitar límites de rate
python 4chandlv15.py "URL" -s 3
```

### Optimización de Rendimiento

**Para boards grandes:**
- Usar `-mt` para procesamiento paralelo
- Configurar `max_workers` entre 3-8
- Usar delay (`-s 1-2`) para evitar bans

**Para conexiones lentas:**
- Reducir `max_workers` a 2-3
- Aumentar delay a 2-3 segundos
- Usar modo secuencial (sin `-mt`)

## Boards Populares

| Board | Descripción | Recomendación |
|-------|-------------|---------------|
| `/g/` | Technology | `-s 1 -mt` |
| `/wg/` | Wallpapers | `-s 2` (imágenes grandes) |
| `/gif/` | GIFs | `-s 1.5` (archivos pesados) |
| `/pol/` | Politics | `-s 2` (muy activo) |
| `/b/` | Random | `-s 1` (rotación rápida) |

## Consejos y Mejores Prácticas

### Evitar Bans

1. **Usar delays apropiados:** 1-3 segundos entre descargas
2. **Limitar workers:** Máximo 5 hilos paralelos
3. **Horarios de menor actividad:** Descargar en madrugada
4. **Pausas entre boards:** Esperar entre diferentes boards

### Optimizar Espacio

```bash
# Deshabilitar creación de índices
python 4chandlv15.py --config-set create_index false

# Saltar hilos ya descargados
python 4chandlv15.py --config-set skip_existing_threads true
```

### Automatización

```bash
#!/bin/bash
# Script para descargar múltiples boards
boards=("g" "wg" "gif")

for board in "${boards[@]}"; do
    python 4chandlv15.py "https://boards.4chan.org/$board/" -mt -s 2
    sleep 60  # Pausa entre boards
done
```

## Changelog

### v16.2 (Actual)
- ✅ Sistema de configuración JSON
- ✅ HTML mejorado con diseño moderno
- ✅ Estadísticas detalladas
- ✅ Índices navegables para boards
- ✅ Manejo mejorado de timeouts
- ✅ Responsive design

### v16.1
- ✅ Soporte para delay entre descargas
- ✅ Prevención de imágenes duplicadas

### v16.0
- ✅ Corrección de nombres de archivo
- ✅ Mejor manejo de errores

## Contribuir

Para reportar bugs o sugerir mejoras, crear un issue con:
- Versión de Python
- Comando ejecutado
- Error completo
- Sistema operativo

## Licencia

MIT License - Uso libre para fines educativos y personales.

---

**⚠️ Disclaimer:** Respetar las reglas de 4chan y usar responsablemente. El autor no se hace responsable del mal uso de esta herramienta.