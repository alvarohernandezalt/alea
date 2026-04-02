# 01 — GUI: Layout y Widgets

> Decisiones de diseno visual para Aleatoric Composer v0.2.
> Framework: PyQt6. Tema oscuro con sistema de diseno Amber/Slate/Teal/Sand.
> Tipografias: DM Serif Display (encabezados), DM Mono (monospace/etiquetas), DM Sans (cuerpo).

---

## 1. Ventana principal

### 1.1 Tamano y proporciones
- Tamano inicial de la ventana: **maximizada** (fullscreen al arrancar)
- Tamano minimo: **1400 x 900 px**
- Redimensionable: **si**
- Pantalla completa permitida: **si** (toggle con F11)

### 1.2 Zonas principales

Se mantienen las **3 zonas** de v0.1, con la misma division por QSplitters arrastrables:

| Zona | Posicion | Contenido |
|------|----------|-----------|
| Sources | Izquierda | Panel de archivos de audio cargados |
| Tabs | Derecha (superior) | Pestanas de configuracion (Composition, Effects, Technique) |
| Timeline | Inferior (ancho completo) | Visualizacion de la composicion generada + mixer |

El QSplitter vertical separa Sources+Tabs (arriba) del Timeline (abajo).
El QSplitter horizontal separa Sources (izquierda) de Tabs (derecha).

```
┌──────────┬─────────────────────────────────┐
│          │  [Composition] [Effects] [Tech]  │
│ SOURCES  │                                  │
│          │  (area de contenido del tab)     │
│ weights  │                                  │
│ waveforms│                                  │
├──────────┴─────────────────────────────────┤
│ [Mixer] ████████ Timeline ████████████████ │
│ [Mixer] ████████████████████████████████── │
│ [Mixer] ████████████████████████████████── │
├────────────────────────────────────────────┤
│ [▶Play] [Render] ═══Progress═══ [WAV][MP3]│
└────────────────────────────────────────────┘
```

### 1.3 Barra de menu

| Menu | Opciones |
|------|----------|
| **File** | Add Audio, Import Config, Export Config, Export Audio, Quit |
| **Composition** | Compose, Re-roll, Render |
| **Technique** | Submenu con las 11 tecnicas + Custom (permite cambio rapido de tecnica sin ir al tab) |
| **Help** | About, Documentation |

Cambios respecto a v0.1:
- **File** se amplia con Import Config / Export Config para guardar y cargar presets completos.
- **Composition** incorpora Render (antes solo estaba en la barra de transporte).
- **Technique** es un menu nuevo que lista las 12 opciones (11 tecnicas + Custom) como accesos directos. Al seleccionar una se actualiza el selector del Tab 3.
- **Help** es nuevo; incluye About (version, creditos) y Documentation (abre la documentacion en navegador o dialog interno).

---

## 2. Panel de Sources (archivos de audio)

### 2.1 Posicion y tamano
- Ubicacion: **lado izquierdo** (SIN CAMBIOS)
- Ancho: **variable**, rango 280-400 px, controlado por QSplitter
- Colapsable: **si** (doble clic en el splitter o boton dedicado)

### 2.2 Informacion por cada source

SIN CAMBIOS respecto a v0.1, con una adicion:

- Nombre del archivo con **indicador de color** (color asignado automaticamente)
- Info tecnica en linea: `duracion | canales | samplerate`
- Mini waveform (visualizacion compacta de la forma de onda)
- Slider de peso (weight) para la probabilidad de seleccion
- **NUEVO:** Icono pequeno junto al nombre indicando la **tecnica activa** aplicada a ese source (recordatorio visual; usa el icono/color de la tecnica del sistema de diseno)

### 2.3 Controles del panel

SIN CAMBIOS:
- **+ Add files**: boton para agregar archivos de audio
- **- Remove**: boton para eliminar el source seleccionado
- **Drag & drop**: se pueden arrastrar archivos desde el explorador al panel

---

## 3. Pestanas / Tabs

### 3.1 Cantidad y nombres

**3 pestanas** (antes 2 en v0.1):

1. **Composition** — configuracion de la estrategia y estructura
2. **Effects Palette** — paleta de efectos de audio
3. **Technique** — seleccion y configuracion de la tecnica compositiva (NUEVO)

### 3.2 Contenido de cada pestana

#### Tab 1: Composition

Controles principales para definir la composicion:

```
┌─────────────────────────────────────────────┐
│  Strategy: [Dropdown selector]              │
│                                             │
│  ── Structure ──────────────────────────    │
│  Duration:  [====|-------|====] min/max     │
│  Tracks:    [====|-------|====] min/max     │
│  Density:   [====|-------|====] min/max     │
│                                             │
│  ── Density Curve ──────────────────────    │
│  Curve: [Dropdown] ┌────────────┐           │
│                     │  /‾‾\      │ preview   │
│                     │ /    \     │           │
│                     └────────────┘           │
│                                             │
│  ── Seed ───────────────────────────────    │
│  Seed: [____________] [Re-roll] [Lock]      │
└─────────────────────────────────────────────┘
```

- **Strategy selector**: dropdown para elegir la estrategia de composicion
- **Structure params**: sliders de rango (RangeSlider con 2 handles) para duracion total, numero de tracks y densidad
- **Density curve**: dropdown para seleccionar tipo de curva + widget de preview que dibuja la forma de la curva seleccionada
- **Seed control**: campo numerico editable, boton Re-roll (genera seed aleatorio), boton Lock (fija el seed)

#### Tab 2: Effects Palette

8 familias de efectos organizadas como **grupos colapsables** (QCollapsible o equivalente):

```
┌─────────────────────────────────────────────┐
│  ▼ Reverb                          [ON/OFF] │
│    Room Size:  [════════●═══] 0.5    [~]    │
│    Damping:    [══●════════] 0.2     [~]    │
│    Wet/Dry:    [═══════●═══] 0.6     [~]    │
│                                             │
│  ▶ Delay (colapsado)               [ON/OFF] │
│  ▶ Filter (colapsado)              [ON/OFF] │
│  ▶ Distortion (colapsado)          [ON/OFF] │
│  ▶ Pitch Shift (colapsado)         [ON/OFF] │
│  ▶ Granular (colapsado)            [ON/OFF] │
│  ▶ Time Stretch (colapsado)        [ON/OFF] │
│  ▶ Dynamics (colapsado)            [ON/OFF] │
└─────────────────────────────────────────────┘
```

Cada familia de efectos contiene:
- **Toggle ON/OFF**: activa o desactiva toda la familia
- **Sliders de parametros**: un slider por parametro con valor numerico visible
- **Boton de aleatorizacion `[~]`**: junto a cada slider, define un rango de randomizacion. Al pulsarlo se expande un mini-control de rango min/max para que el parametro varie estocasticamente entre composiciones

#### Tab 3: Technique (NUEVO)

Configuracion de la tecnica compositiva seleccionada:

```
┌─────────────────────────────────────────────┐
│  Technique: [Dropdown: 11 tecnicas + Custom]│
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ DESCRIPTION CARD                    │    │
│  │ Nombre de la tecnica seleccionada   │    │
│  │ Breve descripcion de su logica      │    │
│  │ compositiva y origen teorico.       │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ── Preset Defaults (read-only) ────────    │
│  param_a: 0.5    param_b: 1.0              │
│  param_c: 0.2    param_d: 3                │
│                                             │
│  ── Overrides ──────────────────────────    │
│  param_a: [════════●═══] 0.7   [Reset]     │
│  param_b: [════●═══════] 0.4   [Reset]     │
│  param_c: (using default)      [Override]   │
│  param_d: (using default)      [Override]   │
│                                             │
└─────────────────────────────────────────────┘
```

- **Technique selector**: dropdown con 12 opciones (11 tecnicas compositivas + Custom). Sincronizado con el menu Technique de la barra de menu
- **Description card**: tarjeta informativa con el nombre, una descripcion breve de la logica compositiva y su fundamentacion teorica. Estilo visual destacado con fondo Teal (#005A65) y texto Sand-20
- **Preset parameter defaults**: seccion de solo lectura que muestra los valores por defecto de cada parametro para la tecnica seleccionada. Sirve como referencia rapida
- **Override controls**: controles editables para cada parametro de la tecnica. Cada parametro puede estar en modo "using default" (usa el preset) o en modo override (slider activo con valor personalizado). Boton [Reset] para volver al default, boton [Override] para activar la edicion

---

## 4. Controles custom (sliders, knobs, visualizadores)

### 4.1 Sliders de rango (min/max)

SIN CAMBIOS en funcionalidad: **RangeSlider** custom con 2 tiradores sobre linea horizontal.

Cambio visual: colores actualizados al sistema de diseno v0.2:
- Track inactivo: Slate-80 (`#3D4A51`)
- Track activo (entre tiradores): Amber (`#FBAD17`)
- Tiradores: Amber con borde Sand-20
- Etiquetas de valor: DM Mono, color Sand-20 (`#E5E1DE`)

### 4.2 Sliders simples

SIN CAMBIOS en funcionalidad. Actualizacion de colores:
- Track: Slate-80 (`#3D4A51`)
- Relleno hasta el valor: gradiente Teal (`#005A65`) a Amber (`#FBAD17`) segun intensidad
- Tirador: Amber (`#FBAD17`)
- Etiqueta de valor: DM Mono, Sand-20

### 4.3 Visualizadores / previews

- **DensityCurvePreview**: SIN CAMBIOS en funcionalidad. Se mantiene el widget que dibuja la curva de densidad seleccionada. Colores actualizados (linea Amber sobre fondo Slate-120)
- **NUEVO: DistributionPreview**: widget compacto (canvas pequeno, aprox. 120x80 px) que muestra la forma de la distribucion estadistica seleccionada para cada parametro de tecnica. Se dibuja la PDF (funcion de densidad de probabilidad) en Teal con relleno semi-transparente. Aparece junto a los sliders del Tab 3 (Technique) cuando el parametro tiene una distribucion asociada

### 4.4 Otros controles especiales

No se introducen controles adicionales en v0.2. Se reservan para futuras versiones:
- Matrices editables (cribas de Xenakis): v0.3+
- Step sequencers: v0.3+
- Random walk visualizers interactivos: v0.3+

---

## 5. Timeline

### 5.1 Diseno del timeline

SIN CAMBIOS en estructura base: lanes horizontales con bloques que representan eventos de audio. Mixer strips a la izquierda.

Cambio visual nuevo:
- **Eventos coloreados por tecnica**: cada bloque en el timeline se colorea segun la tecnica que lo genero, utilizando el color asignado a esa tecnica en el sistema de diseno. Esto reemplaza el esquema anterior donde los bloques se coloreaban solo por source

### 5.2 Mixer strips

SIN CAMBIOS: cada track tiene los siguientes controles en su mixer strip:
- **Nombre** del track
- **Mute** (M) — silencia el track
- **Solo** (S) — aisla el track
- **Volume** — slider vertical
- **Pan** — slider horizontal

### 5.3 Interaccion

- Arrastrar bloques en el timeline: **no** (read-only en v0.2)
- Seleccionar eventos individuales: **no** (read-only en v0.2)
- Zoom horizontal: **si** (Ctrl + scroll del raton)
- Zoom vertical: **no** (solo horizontal en v0.2)

El timeline es de **solo lectura** en v0.2. La edicion directa de eventos (drag, resize, split) se pospone a v0.3.

---

## 6. Transport / barra inferior

Barra de transporte ubicada en la parte inferior de la ventana, debajo del timeline:

```
┌────────────────────────────────────────────────────────┐
│ [▶ Play] [■ Stop] [Render] ═══Progress Bar═══ [WAV] [MP3] │
│                              00:00 / 03:45             │
└────────────────────────────────────────────────────────┘
```

Cambios respecto a v0.1:

| Control | Estado |
|---------|--------|
| Render | SIN CAMBIOS — inicia el proceso de renderizado |
| Progress Bar | SIN CAMBIOS — muestra progreso de render/export |
| Export WAV | SIN CAMBIOS |
| Export MP3 | SIN CAMBIOS |
| **Play/Stop** | **NUEVO** — botones para preescuchar la composicion renderizada. Play inicia reproduccion, Stop la detiene. Deshabilitados si no hay render disponible |
| **Indicador de tiempo** | **NUEVO** — muestra posicion actual / duracion total en formato `MM:SS / MM:SS`. Se actualiza en tiempo real durante la reproduccion |

---

## 7. Tema visual (colores, tipografia)

### 7.1 Colores

Se **mantiene el dark theme** pero se reemplaza la paleta completa con el sistema de diseno v0.2:

| Rol | Color | Hex |
|-----|-------|-----|
| Background (fondo principal) | Slate-120 | `#1E282D` |
| Panels (fondo de paneles) | Slate-100 | `#303C42` |
| Borders (bordes, separadores) | Slate-80 | `#3D4A51` |
| Text (texto principal) | Sand-20 | `#E5E1DE` |
| Muted text (texto secundario) | Sand-60 | `#B9AFA9` |
| Accent primary (acento principal) | Amber | `#FBAD17` |
| Accent secondary (acento secundario) | Teal | `#005A65` |
| Disabled / inactive | Sand | `#A69C95` al 40% opacidad |
| Error / warning | Amber saturado | `#FF8C00` |
| Success / active | Teal claro | `#00897B` |

### 7.2 Tipografia

| Uso | Fuente | Peso | Tamano |
|-----|--------|------|--------|
| Encabezados de seccion | DM Serif Display | Regular | 16-20 px |
| Etiquetas de controles | DM Mono | Regular | 12 px |
| Valores numericos | DM Mono | Medium | 12 px |
| Texto de cuerpo / descripciones | DM Sans | Regular | 13 px |
| Nombres de tabs | DM Sans | Medium | 13 px |
| Barra de menu | DM Sans | Regular | 13 px |
| Tooltips | DM Sans | Regular | 11 px |

### 7.3 Aplicacion del stylesheet

Se implementa via `QApplication.setStyleSheet()` con un stylesheet global que define:
- Colores de fondo, texto y bordes para todos los widgets base
- Estilos especificos para `QTabWidget`, `QSplitter`, `QSlider`, `QMenuBar`, `QToolBar`
- Pseudo-estados: `:hover` usa Amber al 20% sobre el fondo, `:pressed` usa Amber al 40%, `:disabled` aplica opacidad reducida

---

## 8. Bocetos de referencia

No se incluyen bocetos a mano en esta version. El layout ASCII de la seccion 1.2 y los diagramas de cada tab en la seccion 3.2 sirven como referencia de diseno para la implementacion.
