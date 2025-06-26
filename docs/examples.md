# Ejemplos Prácticos - 4chan Downloader

## Casos de Uso Comunes

### 1. Descarga Rápida de un Hilo

```bash
# Hilo simple sin delay
python 4chandlv15.py "https://boards.4chan.org/g/thread/98765432"

# Resultado: Descarga en ~30 segundos
# Archivos: 4chan_downloader/g/98765432_Thread_Subject/
```

### 2. Board Completo para Archivo

```bash
# Board de wallpapers con delay
python 4chandlv15.py "https://boards.4chan.org/wg/" -s 2 -t dark

# Tiempo estimado: 2-4 horas para ~150 hilos
# Tamaño típico: 1-5 GB dependiendo del board
```

### 3. Descarga Masiva Optimizada

```bash
# Configurar para máximo rendimiento
python 4chandlv15.py --config-set max_workers 8
python 4chandlv15.py --config-set default_sleep 1

# Descargar con configuración optimizada
python 4chandlv15.py "https://boards.4chan.org/g/" -mt
```

## Scripts de Automatización

### Script Básico para Múltiples Boards

```bash
#!/bin/bash
# download_boards.sh

echo "🚀 Iniciando descarga de boards múltiples..."

boards=("wg" "gif" "hr")
delay=2

for board in "${boards[@]}"; do
    echo "📋 Procesando /$board/..."
    python 4chandlv15.py "https://boards.4chan.org/$board/" -mt -s $delay -t dark
    
    echo "⏸️  Pausa de 2 minutos entre boards..."
    sleep 120
done

echo "✅ Descarga completa!"
```

### Script con Manejo de Errores

```bash
#!/bin/bash
# robust_download.sh

SCRIPT_PATH="4chandlv15.py"
LOG_FILE="download_$(date +%Y%m%d_%H%M%S).log"

download_with_retry() {
    local url=$1
    local max_retries=3
    local retry=0
    
    while [ $retry -lt $max_retries ]; do
        echo "🔄 Intento $((retry + 1)) para $url" | tee -a $LOG_FILE
        
        if python $SCRIPT_PATH "$url" -mt -s 2 2>&1 | tee -a $LOG_FILE; then
            echo "✅ Éxito: $url" | tee -a $LOG_FILE
            return 0
        else
            echo "❌ Error en intento $((retry + 1))" | tee -a $LOG_FILE
            retry=$((retry + 1))
            sleep 60
        fi
    done
    
    echo "💀 Falló después de $max_retries intentos: $url" | tee -a $LOG_FILE
    return 1
}

# Uso
download_with_retry "https://boards.4chan.org/g/"
```

## Configuraciones por Tipo de Board

### Boards de Imágenes (wg, hr, p)

```bash
# Configuración para wallpapers y fotos
python 4chandlv15.py --config-set max_workers 3
python 4chandlv15.py --config-set default_sleep 2

# Descarga
python 4chandlv15.py "https://boards.4chan.org/wg/" -mt -t dark
```

### Boards de Discusión (g, pol, b)

```bash
# Configuración para boards muy activos
python 4chandlv15.py --config-set max_workers 2
python 4chandlv15.py --config-set default_sleep 3

# Descarga con máximo cuidado
python 4chandlv15.py "https://boards.4chan.org/g/" -s 3
```

### Boards de Media Pesado (gif, wsg)

```bash
# Para archivos grandes
python 4chandlv15.py --config-set max_workers 2
python 4chandlv15.py --config-set default_sleep 2.5

python 4chandlv15.py "https://boards.4chan.org/gif/" -mt -s 2.5
```

## Mantenimiento y Organización

### Script de Limpieza

```bash
#!/bin/bash
# cleanup.sh - Limpia archivos antiguos

DOWNLOAD_DIR="4chan_downloader"
DAYS_OLD=30

echo "🧹 Limpiando archivos mayores a $DAYS_OLD días..."

find $DOWNLOAD_DIR -type f -mtime +$DAYS_OLD -name "*.html" -delete
find $DOWNLOAD_DIR -type f -mtime +$DAYS_OLD -name "*.json" -delete

# Limpiar carpetas vacías
find $DOWNLOAD_DIR -type d -empty -delete

echo "✅ Limpieza completada"
```

### Backup de Configuración

```bash
#!/bin/bash
# backup_config.sh

CONFIG_FILE="4chan_config.json"
BACKUP_DIR="backups"

mkdir -p $BACKUP_DIR

if [ -f $CONFIG_FILE ]; then
    cp $CONFIG_FILE "$BACKUP_DIR/config_backup_$(date +%Y%m%d_%H%M%S).json"
    echo "✅ Configuración respaldada"
else
    echo "❌ No se encontró archivo de configuración"
fi
```

## Monitoreo y Logs

### Script con Logging Detallado

```bash
#!/bin/bash
# monitor_download.sh

LOG_DIR="logs"
mkdir -p $LOG_DIR

LOG_FILE="$LOG_DIR/download_$(date +%Y%m%d).log"
STATS_FILE="$LOG_DIR/stats_$(date +%Y%m%d).json"

{
    echo "=== Inicio de sesión: $(date) ==="
    echo "URL: $1"
    echo "Configuración actual:"
    python 4chandlv15.py --config-show
    echo "=========================="
    
    # Medir tiempo de ejecución
    start_time=$(date +%s)
    python 4chandlv15.py "$1" -mt -s 2
    end_time=$(date +%s)
    
    duration=$((end_time - start_time))
    echo "Tiempo total: ${duration}s"
    echo "=== Fin de sesión: $(date) ==="
    
} 2>&1 | tee -a $LOG_FILE
```

## Troubleshooting Específico

### Problema: Downloads Muy Lentos

```bash
# Diagnóstico
python 4chandlv15.py --config-show

# Solución: Reducir workers y aumentar delay
python 4chandlv15.py --config-set max_workers 2
python 4chandlv15.py --config-set default_sleep 3
```

### Problema: Muchos Errores 403/429

```bash
# Configuración conservadora
python 4chandlv15.py --config-set max_workers 1
python 4chandlv15.py --config-set default_sleep 5

# Descarga secuencial
python 4chandlv15.py "URL" -s 5  # Sin -mt
```

### Problema: Archivos Corruptos

```bash
# Forzar re-descarga
python 4chandlv15.py "URL" --overwrite -s 2
```

## Casos de Uso Especiales

### Archivar Board Completo Antes de que Cierre

```bash
#!/bin/bash
# emergency_archive.sh

BOARD="$1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_DIR="emergency_archive_${BOARD}_${TIMESTAMP}"

echo "🚨 ARCHIVO DE EMERGENCIA: /$BOARD/"

# Configuración rápida pero segura
python 4chandlv15.py --config-set max_workers 4
python 4chandlv15.py --config-set default_sleep 1

# Descarga con log completo
python 4chandlv15.py "https://boards.4chan.org/$BOARD/" -mt -s 1 2>&1 | tee "emergency_${BOARD}_${TIMESTAMP}.log"

echo "📦 Archivo completado en: $ARCHIVE_DIR"
```

### Monitoreo de Hilo Específico

```bash
#!/bin/bash
# monitor_thread.sh

THREAD_URL="$1"
CHECK_INTERVAL=300  # 5 minutos

while true; do
    echo "🔍 Verificando hilo: $(date)"
    
    if python 4chandlv15.py "$THREAD_URL" -s 1; then
        echo "✅ Hilo actualizado"
    else
        echo "❌ Error o hilo caído"
        break
    fi
    
    sleep $CHECK_INTERVAL
done
```

## Optimización por Hardware

### Para SSD Rápido

```bash
python 4chandlv15.py --config-set max_workers 8
python 4chandlv15.py --config-set default_sleep 0.5
```

### Para HDD o Conexión Lenta

```bash
python 4chandlv15.py --config-set max_workers 2
python 4chandlv15.py --config-set default_sleep 3
```

### Para VPS/Server

```bash
python 4chandlv15.py --config-set max_workers 6
python 4chandlv15.py --config-set default_sleep 1.5
```