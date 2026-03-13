# Aleatoric Composer para la Escuela SUR (beta)

Aplicacion de escritorio para composicion semi-aleatoria de audio. Toma archivos de audio, les aplica procesos (granulares, espectrales, efectos clasicos) y monta composiciones multipista usando metodos semi-aleatorios con control variable. El resultado se exporta como WAV o MP3.

(c) Alvaro Hernandez Altozano 2026

---

## Descarga e instalacion

### Windows 11

1. Ve a la seccion [Releases](https://github.com/alvarohernandezalt/aleatoric-composer/releases) de este repositorio
2. Descarga `AleatoricComposer-Windows.zip`
3. Descomprime el ZIP en cualquier carpeta
4. Ejecuta `AleatoricComposer.exe`

> **Nota sobre SmartScreen**: La primera vez que ejecutes el .exe, Windows puede mostrar un aviso de "Windows protegió su equipo". Haz click en "Mas informacion" y luego en "Ejecutar de todas formas". Esto es normal para aplicaciones sin firma digital y solo ocurre la primera vez.

### macOS (Sonoma / Sequoia - Apple Silicon)

1. Ve a la seccion [Releases](https://github.com/alvarohernandezalt/aleatoric-composer/releases) de este repositorio
2. Descarga `AleatoricComposer-macOS.zip`
3. Descomprime el ZIP
4. Haz **click derecho** sobre `AleatoricComposer.app` y selecciona **"Abrir"**
5. En el dialogo de seguridad, haz click en **"Abrir"** de nuevo

> **Nota sobre Gatekeeper**: Como la app no esta firmada con un Apple Developer ID, macOS la bloquea por defecto. Usar click derecho > Abrir evita este bloqueo. Solo es necesario la primera vez.

### No necesitas instalar nada mas

Los ejecutables incluyen Python, todas las librerias de audio y la interfaz grafica. No necesitas tener Python, pip ni ninguna dependencia instalada.

---

## Como usar la aplicacion

### 1. Cargar archivos de audio

- Haz click en **"+ Add files"** en el panel izquierdo, o arrastra archivos de audio directamente
- Formatos soportados: WAV, MP3, FLAC, OGG, AIFF

### 2. Configurar la composicion

En la pestana **Composition** (panel derecho):

- **Strategy** (Estrategia): elige como se organizan los fragmentos
  - **Scatter**: fragmentos dispersos aleatoriamente (resultado mas caotico)
  - **Structured**: secciones con transiciones (sparse / dense / climax / silence)
  - **Layer**: texturas continuas y drones
  - **Canon**: material repetido con offset temporal entre tracks
- **Seed**: semilla aleatoria. La misma semilla con los mismos archivos produce siempre el mismo resultado
- **Duration**: duracion total de la pieza en segundos
- **Tracks**: numero de pistas simultaneas (1-16)

### 3. Ajustar parametros

- **Timing**: duracion de los eventos y silencios entre ellos
- **Dynamics**: rango de amplitud, panorama, fades
- **Effects**: probabilidad de aplicar efectos y cuales usar
- **Density curve**: como evoluciona la densidad de eventos a lo largo del tiempo

### 4. Componer

- Click en **"Compose"** para generar la composicion
- El timeline inferior se llenara de eventos coloreados (un color por archivo fuente)
- Click en **"Re-roll"** para generar una variacion diferente

### 5. Renderizar y exportar

- Click en **"Render"** para procesar el audio (la barra de progreso muestra el avance)
- Click en **"Export WAV"** o **"Export MP3"** para guardar el resultado

---

## Efectos disponibles

### Efectos clasicos (via Pedalboard)
Reverb, Delay, Chorus, Phaser, Distortion, Bitcrush, Compressor, Ladder Filter, Pitch Shift, Gain, y mas.

### Efectos avanzados
- **Granular Synth**: rompe el audio en granos pequenos y los reensambla con control de densidad, pitch, posicion y ventana
- **Spectral Freeze**: congela el espectro en un punto temporal para crear drones
- **Spectral Smear**: difumina el espectro aplicando blur gaussiano
- **Spectral Gate**: elimina componentes frecuenciales por debajo de un umbral
- **Spectral Shift**: desplaza todas las frecuencias arriba o abajo
- **Time Stretch**: cambia la duracion sin alterar el pitch

---

## Seguridad

Esta aplicacion esta disenada para funcionar **100% offline**:

- No contiene ningun codigo de red (no usa socket, requests, urllib ni ninguna libreria de red)
- Incluye un bloqueo a nivel de runtime que impide cualquier conexion de red saliente
- No envia telemetria, analytics ni datos de ningun tipo
- No se conecta a internet bajo ningun concepto

Los modulos de red de PySide6 (QtNetwork, QtWebEngine, QtWebSockets) han sido excluidos del ejecutable.

---

## Informacion tecnica

### Stack
- **Python 3.12** + **PySide6** (interfaz grafica)
- **Pedalboard** (Spotify) para efectos de audio profesionales
- **Librosa** para analisis espectral y phase vocoder
- **NumPy / SciPy** para procesamiento de senales custom
- **PyInstaller** para compilacion a ejecutable standalone

### Compilacion desde codigo fuente

Si quieres compilar tu propia version:

```bash
# Clonar repositorio
git clone https://github.com/alvarohernandezalt/aleatoric-composer.git
cd aleatoric-composer

# Crear entorno virtual (Python 3.12 recomendado)
python -m venv .venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Instalar dependencias
pip install -r requirements.txt
pip install pyinstaller

# Ejecutar desde codigo
python -m src.main

# Compilar ejecutable
pyinstaller aleatoric_composer.spec
# Resultado en dist/AleatoricComposer/
```

### Requisitos para exportar MP3
La exportacion a MP3 requiere [FFmpeg](https://ffmpeg.org/) instalado y en el PATH del sistema.

---

## Licencia

(c) Alvaro Hernandez Altozano 2026. Todos los derechos reservados.
