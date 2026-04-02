# 00 — Medidas del Layout Actual (v0.1) — Referencia en Píxeles

> Auditoría exhaustiva de TODAS las dimensiones, márgenes, paddings, fuentes,
> radios de borde y medidas de pintura custom del GUI actual.
> Resolución de referencia: **pantalla completa** (la app debe abrirse maximizada).

---

## 0. Ventana principal

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Tamaño mínimo | **1200 × 800 px** | main_window.py:71 |
| Tamaño inicial (resize) | **1400 × 900 px** | main_window.py:72 |
| Márgenes del layout central | **0, 0, 0, 0** | main_window.py:124 |
| Spacing del layout central | **0** | main_window.py:125 |

> **Nota:** Para v0.2 la ventana debe abrirse **maximizada** (toda la pantalla).
> En un monitor 1920×1080, el espacio útil (sin taskbar ~40px) es ~1920×1040.

---

## 1. Splitters (divisores arrastrables)

### 1.1 Splitter horizontal (Sources | Tabs)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Tamaños iniciales | **[300, 700]** px | main_window.py:148 |
| Ancho del handle | **3 px** | theme.py:221 |

**Panel izquierdo (Sources):**
| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Ancho mínimo | **280 px** | main_window.py:135 |
| Ancho máximo | **400 px** | main_window.py:136 |

**Panel derecho (Tabs):**
| Propiedad | Valor |
|-----------|-------|
| Ancho inicial | **700 px** (el resto del splitter) |
| Sin límites explícitos | Crece/encoge con la ventana |

### 1.2 Splitter vertical (Tabs+Sources | Timeline)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Tamaños iniciales | **[450, 350]** px | main_window.py:156 |
| Alto del handle | **3 px** | theme.py:225 |

> En pantalla completa 1920×1040:
> - Zona superior (Sources + Tabs): ~**575 px** alto (proporcional)
> - Zona inferior (Timeline + Transport): ~**465 px** alto (proporcional)

---

## 2. Panel de Sources (columna izquierda)

### 2.1 Layout general del panel

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Márgenes internos | **4, 4, 4, 4 px** | source_panel.py:69 |

### 2.2 Header "SOURCES"

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Font size | **14px** | source_panel.py:73 |
| Font weight | **bold** | source_panel.py:73 |

### 2.3 Lista de archivos

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto mínimo | **100 px** | source_panel.py:89 |

### 2.4 SourceItemWidget (cada archivo en la lista)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Márgenes layout | **4, 4, 4, 4 px** | source_panel.py:37 |
| Spacing layout | **2 px** | source_panel.py:38 |
| Nombre del source — font | **12px bold** | source_panel.py:42 |
| Info técnica — font | **11px** (secondary) | source_panel.py:47–49 |
| Waveform mini — alto fijo | **35 px** | source_panel.py:54 |

### 2.5 Sección de pesos (Weights)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Label "Weights" — font | **11px bold** | source_panel.py:94 |
| Label "Weights" — margin-top | **8 px** | source_panel.py:94 |
| Scroll area — alto máximo | **150 px** | source_panel.py:99 |
| Layout interno — márgenes | **0, 0, 0, 0** | source_panel.py:102 |
| Layout interno — spacing | **2 px** | source_panel.py:103 |

### 2.6 Fila de peso por source

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Nombre label — ancho fijo | **90 px** | source_panel.py:163 |
| Nombre label — font | **11px** | source_panel.py:164 |
| Slider — rango | **0–100** | source_panel.py:168 |
| Slider — ocupa stretch restante | (flexible) | — |
| Valor label — ancho fijo | **35 px** | source_panel.py:173 |
| Valor label — font | **11px** | source_panel.py:174 |

---

## 3. Pestañas (Tabs) — panel derecho superior

### 3.1 Dimensiones del TabBar

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Padding de cada tab | **8px 18px** (vertical/horizontal) | theme.py:158 |
| Border-radius superior | **4px** (izq y der) | theme.py:161–162 |
| Margen derecho entre tabs | **2 px** | theme.py:163 |
| Borde inferior tab seleccionado | **2px solid ACCENT** | theme.py:169 |

### 3.2 Tab "Composition"

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Layout spacing | **8 px** | composition_panel.py:40 |

#### 3.2.1 Seed

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Botón "Random" — ancho fijo | **70 px** | composition_panel.py:62 |

#### 3.2.2 RangeSliders (duración, silencio, amplitud, pan, fade-in, fade-out)

Cada RangeSlider tiene las mismas dimensiones:

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto mínimo | **36 px** | parameter_controls.py:122 |
| Alto máximo | **36 px** (fijo) | parameter_controls.py:123 |
| Offset izquierdo del track | **130 px** | parameter_controls.py:140 |
| Offset derecho del track | **width − 60 px** | parameter_controls.py:141 |
| Ancho del label de nombre | **125 px** | parameter_controls.py:161 |
| Ancho del valor numérico | **55 px** | parameter_controls.py:185 |
| Radio del handle (punto) | **7 px** (diámetro 14px) | parameter_controls.py:120 |
| Grosor track inactivo | **2 px** | parameter_controls.py:164 |
| Grosor track activo (rango) | **3 px** | parameter_controls.py:172 |
| Color track inactivo | **#444466** | parameter_controls.py:166 |
| Color track activo | **#7c6ff0** (ACCENT) | parameter_controls.py:172 |
| Color handle relleno | **#7c6ff0** | parameter_controls.py:177 |
| Color handle borde | **#e0e0e0** | parameter_controls.py:178 |

#### 3.2.3 LabeledSlider (sliders simples: probabilidad, etc.)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Márgenes layout | **0, 0, 0, 0** | parameter_controls.py:47–48 |
| Ancho del label | **120 px** | parameter_controls.py:51 |
| Color del label | **#bbbbcc** | parameter_controls.py:52 |
| Slider — ocupa stretch | (flexible) | parameter_controls.py:59 |
| Pasos internos del slider | **1000** | parameter_controls.py:56 |
| Ancho del valor numérico | **70 px** | parameter_controls.py:62 |
| Color del valor | **#e0e0e0** | parameter_controls.py:64 |

#### 3.2.4 DensityCurvePreview

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto fijo | **70 px** | parameter_controls.py:230 |
| Ancho mínimo | **180 px** | parameter_controls.py:231 |
| Margen del plot | **8 px** (todos los lados) | parameter_controls.py:244 |
| Puntos de la curva | **100** | parameter_controls.py:254 |
| Grosor de la curva | **2 px** | parameter_controls.py:269 |
| Escala vertical | **0.45×** | parameter_controls.py:260 |
| Color del fondo | **#1e1e2e** | parameter_controls.py:240 |
| Color del grid | **#333355** (línea punteada) | parameter_controls.py:249 |
| Color de la curva | **#7c6ff0** (ACCENT) | parameter_controls.py:269 |
| Label — font | **8pt** | parameter_controls.py:275 |
| Label — color | **#8888aa** | parameter_controls.py:273 |
| Label — rectángulo | **margin, 2, plot_w, 14 px** | parameter_controls.py:277 |

#### 3.2.5 Botones de acción

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| "Compose" — alto mínimo | **36 px** | composition_panel.py:160 |
| "Re-roll" — alto mínimo | **36 px** | composition_panel.py:165 |

### 3.3 Tab "Effects Palette"

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Layout spacing | **8 px** | effects_panel.py:107 |
| Header "EFFECTS PALETTE" — font | **14px bold** | effects_panel.py:111 |
| Info label | objectName="secondary" → **11px** | effects_panel.py:115 |
| Param controls spacing | **4 px** | effects_panel.py:132 |

---

## 4. Timeline (zona inferior)

### 4.1 Layout general

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Márgenes del timeline layout | **0, 0, 0, 0** | timeline_view.py:239 |
| Spacing | **0** | timeline_view.py:240 |
| Spacing del content layout | **0** | timeline_view.py:244 |

### 4.2 Mixer Strips (columna izquierda del timeline)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Ancho del scroll area | **85 px** | timeline_view.py:248 |
| Ancho de cada MixerStrip | **80 px** | timeline_view.py:33 |
| Márgenes del strip | **2, 4, 2, 4 px** | timeline_view.py:36 |
| Spacing del strip | **3 px** | timeline_view.py:37 |
| Offset superior (alinear con ruler) | **20 px** top margin | timeline_view.py:252 |

#### Controles de cada MixerStrip:

| Control | Tamaño | Archivo:Línea |
|---------|--------|---------------|
| Nombre del track — font | **11px bold** | timeline_view.py:42 |
| Botón Mute [M] | **30 × 22 px** | timeline_view.py:49 |
| Botón Mute — font | **10px** | timeline_view.py:50 |
| Botón Solo [S] | **30 × 22 px** | timeline_view.py:56 |
| Botón Solo — font | **10px** | timeline_view.py:57 |
| Slider Volume (vertical) | alto fijo **60 px** | timeline_view.py:67 |
| Slider Volume — rango | **0–100** | timeline_view.py:65 |
| Slider Pan (horizontal) | (sin alto fijo, stretch) | timeline_view.py:74 |
| Slider Pan — rango | **−100 a +100** | timeline_view.py:74 |

### 4.3 TimelineCanvas (área de eventos)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto mínimo | **100 px** | timeline_view.py:109 |
| Alto dinámico | **max(200, tracks × 55 + 40) px** | timeline_view.py:120 |

#### Regla temporal (ruler):

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto de la regla | **20 px** | timeline_view.py:147 |
| Tick marks — alto | **4 px** (de ruler_h−4 a ruler_h) | timeline_view.py:152 |
| Labels — offset | **−15px X, −5px Y** desde el tick | timeline_view.py:153 |
| Labels — font | **9pt** | timeline_view.py:144 |

#### Tracks (lanes):

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto de cada track | **55 px** | timeline_view.py:106 |
| Separador entre tracks | **1 px** línea | timeline_view.py:165–166 |
| Color alternante | **#2a2a3e** vs **BG_PANEL** | timeline_view.py:161 |

#### Eventos (bloques en el timeline):

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto del evento | **track_height − 6 = 49 px** | timeline_view.py:177 |
| Offset vertical del evento | **3 px** desde el top del track | timeline_view.py:177 |
| Borde del rectángulo | **1 px** | timeline_view.py:193 |
| Fill alpha | **160/255 (~63%)** | timeline_view.py:188 |
| Border alpha | **220/255 (~86%)** | timeline_view.py:194 |
| Label — padding | **3px izq, 2px top, 6px der, 4px bottom** | timeline_view.py:207–211 |
| Label — font | **8pt** | timeline_view.py:200 |
| Label — color | **#ffffff** | timeline_view.py:198 |

#### Zoom y scroll:

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Zoom inicial | **8.0 px/segundo** | timeline_view.py:105 |
| Zoom mínimo | **1.0 px/s** | timeline_view.py:218 |
| Zoom máximo | **200.0 px/s** | timeline_view.py:218 |
| Scroll velocity | **delta × 0.5** | timeline_view.py:222–223 |

### 4.4 Stats bar (barra inferior del timeline)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Padding | **4px 8px** | timeline_view.py:270 |
| Borde superior | **1px solid #3a3a55** | timeline_view.py:270 |

---

## 5. Transport bar (barra inferior de la ventana)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Márgenes del layout | **8, 4, 8, 4 px** | main_window.py:161 |
| Background | **#252536** | main_window.py:185 |
| Borde superior | **1px solid #3a3a55** | main_window.py:185 |

| Control | Tamaño | Archivo:Línea |
|---------|--------|---------------|
| Botón Render — alto mínimo | **32 px** | main_window.py:165 |
| Progress bar — alto fijo | **22 px** | main_window.py:172 |
| Copyright label — font | **11px** | main_window.py:190 |
| Copyright label — padding | **4 px** | main_window.py:190 |

---

## 6. Waveform widget (genérico)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto mínimo | **30 px** | waveform_view.py:26 |
| Alto máximo | **60 px** | waveform_view.py:27 |
| En source panel — alto fijo | **35 px** | source_panel.py:54 |
| Puntos de muestreo | **200** | waveform_view.py:19 |
| Grosor del trazo | **1.0 px** | waveform_view.py:79 |
| Alpha del relleno | **80/255 (~31%)** | waveform_view.py:83 |
| Margen de amplitud | **2 px** (mid_y − 2) | waveform_view.py:95 |
| Color por defecto | **#4ecdc4** | waveform_view.py:23 |
| Fondo por defecto | **#1e1e2e** | waveform_view.py:24 |

---

## 7. Controles estándar Qt (stylesheet global)

### 7.1 QPushButton

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Padding | **6px 14px** | theme.py:57 |
| Alto mínimo | **24 px** | theme.py:58 |
| Border-radius | **4 px** | theme.py:56 |
| Variante accent — font-weight | **bold** | theme.py:74 |
| Variante accent — border | **none** | theme.py:75 |
| Hover accent — color | **#8b7ff0** | theme.py:79 |

### 7.2 QSlider (horizontal, estándar Qt)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Groove — alto | **4 px** | theme.py:113 |
| Groove — border-radius | **2 px** | theme.py:115 |
| Handle — ancho | **14 px** | theme.py:120 |
| Handle — alto | **14 px** | theme.py:121 |
| Handle — margin | **−5px 0** | theme.py:122 |
| Handle — border-radius | **7 px** (circular) | theme.py:123 |
| Sub-page — border-radius | **2 px** | theme.py:128 |

### 7.3 QComboBox

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Padding | **4px 8px** | theme.py:87 |
| Alto mínimo | **24 px** | theme.py:88 |
| Border-radius | **4 px** | theme.py:86 |
| Drop-down — ancho | **24 px** | theme.py:93 |

### 7.4 QSpinBox / QDoubleSpinBox

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Padding | **3px 6px** | theme.py:108 |
| Alto mínimo | **22 px** | theme.py:109 |
| Border-radius | **4 px** | theme.py:107 |

### 7.5 QCheckBox

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Spacing (entre caja y texto) | **8 px** | theme.py:133 |
| Indicator — ancho | **16 px** | theme.py:137 |
| Indicator — alto | **16 px** | theme.py:138 |
| Indicator — border-radius | **3 px** | theme.py:140 |

### 7.6 QGroupBox

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Border-radius | **6 px** | theme.py:38 |
| Margin-top | **10 px** | theme.py:39 |
| Padding-top | **18 px** | theme.py:40 |
| Font-weight | **bold** | theme.py:41 |
| Título — left | **12 px** | theme.py:47 |
| Título — padding | **0 6px** | theme.py:48 |

### 7.7 QScrollBar (vertical)

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Ancho | **10 px** | theme.py:179 |
| Handle — min-height | **30 px** | theme.py:186 |
| Handle — border-radius | **5 px** | theme.py:185 |

### 7.8 QProgressBar

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Alto mínimo | **18 px** | theme.py:208 |
| Border-radius | **4 px** | theme.py:205 |
| Chunk — border-radius | **3 px** | theme.py:213 |

### 7.9 QListWidget

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Border-radius | **4 px** | theme.py:231 |
| Item — padding | **4 px** | theme.py:236 |
| Item — border-bottom | **1px solid BORDER** | theme.py:237 |
| Item seleccionado — border-left | **3px solid ACCENT** | theme.py:242 |

### 7.10 QSplitter handles

| Propiedad | Valor | Archivo:Línea |
|-----------|-------|---------------|
| Handle horizontal — ancho | **3 px** | theme.py:221 |
| Handle vertical — alto | **3 px** | theme.py:225 |
| Color del handle | **BORDER (#3a3a55)** | theme.py:222, 226 |

---

## 8. Paleta de colores completa

### 8.1 Constantes del tema

| Nombre | Hex | Uso |
|--------|-----|-----|
| BG_WINDOW | **#1e1e2e** | Fondo principal de la ventana |
| BG_PANEL | **#252536** | Fondo de paneles y contenedores |
| BG_CONTROL | **#2d2d44** | Fondo de controles (botones, combos) |
| BG_INPUT | **#363650** | Fondo de inputs (spinbox, text) |
| TEXT_PRIMARY | **#e0e0e0** | Texto principal |
| TEXT_SECONDARY | **#8888aa** | Texto secundario / labels |
| ACCENT | **#7c6ff0** | Color de acento principal (púrpura) |
| ACCENT2 | **#4ecdc4** | Color de acento secundario (turquesa) |
| BORDER | **#3a3a55** | Bordes y separadores |
| HOVER | **#3d3d5c** | Estado hover |

### 8.2 Paleta de colores de tracks

| Índice | Hex | Color |
|--------|-----|-------|
| 0 | **#4ecdc4** | Turquesa |
| 1 | **#ff6b6b** | Coral |
| 2 | **#ffd93d** | Amarillo |
| 3 | **#6bcb77** | Verde |
| 4 | **#a78bfa** | Lavanda |
| 5 | **#f472b6** | Rosa |
| 6 | **#fb923c** | Naranja |
| 7 | **#38bdf8** | Azul cielo |

### 8.3 Colores inline (fuera de theme.py)

| Color | Uso | Archivo:Línea |
|-------|-----|---------------|
| #2a2a3e | Track alterno en timeline | timeline_view.py:161 |
| #888888 | Color fallback por defecto | timeline_view.py:183 |
| #ffffff | Texto de event labels | timeline_view.py:198 |
| #444466 | Track inactivo del RangeSlider | parameter_controls.py:166 |
| #bbbbcc | Labels de LabeledSlider | parameter_controls.py:160 |
| #333355 | Grid del DensityCurvePreview | parameter_controls.py:249 |
| #8b7ff0 | Hover del accent button | theme.py:79 |

---

## 9. Tipografía completa

| Contexto | Familia | Tamaño | Peso | Archivo:Línea |
|----------|---------|--------|------|---------------|
| **Base global** | Segoe UI, Arial, sans-serif | **13px** | normal | theme.py:31–32 |
| Headers (SOURCES, EFFECTS) | — | **14px** | **bold** | source_panel.py:73, effects_panel.py:111 |
| Source name | — | **12px** | **bold** | source_panel.py:42 |
| Track name (mixer) | — | **11px** | **bold** | timeline_view.py:42 |
| Labels secundarios | — | **11px** | normal | theme.py:199 |
| Controles M/S | — | **10px** | normal | timeline_view.py:50, 57 |
| Ruler del timeline | — | **9pt** | normal | timeline_view.py:144 |
| Event labels | — | **8pt** | normal | timeline_view.py:200 |
| Curve label | — | **8pt** | normal | parameter_controls.py:275 |
| Copyright | — | **11px** | normal | main_window.py:190 |

---

## 10. Mapa de layout a pantalla completa (1920 × 1040)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MENU BAR  (File | Composition)                           ~30px alto        │
├────────────┬─────────────────────────────────────────────────────────────────┤
│            │                                                                │
│  SOURCES   │   TABS  (Composition | Effects Palette)                        │
│            │                                                                │
│  280–400px │   ~1520–1640px ancho                                           │
│  ancho     │                                                                │
│            │   Contiene: GroupBoxes con RangeSliders (36px alto c/u),        │
│   ~575px   │   LabeledSliders, DensityCurvePreview (70px alto),             │
│   alto     │   ComboBoxes (24px alto), Botones Compose/Reroll (36px alto)   │
│            │                                                                │
│  ┌──────┐  │                                                                │
│  │wave  │  │                                                                │
│  │35px  │  │                                                                │
│  ├──────┤  │                                                                │
│  │pesos │  │                                                                │
│  │≤150px│  │                                                                │
│  └──────┘  │                                                                │
│ splitter 3px                                                                │
├────────────┴─────────────────────────────────────────────────────────────────┤
│ TIMELINE                                                         ~435px alto│
│ ┌────────┬───────────────────────────────────────────────────────────────┐   │
│ │ MIXER  │  RULER (20px alto)                                           │   │
│ │ 85px   ├──────────────────────────────────────────────────────────────┤   │
│ │ ancho  │  TRACK 1 (55px alto, eventos 49px)                          │   │
│ │        ├──────────────────────────────────────────────────────────────┤   │
│ │ M[30×22]  TRACK 2 (55px alto)                                        │   │
│ │ S[30×22]──────────────────────────────────────────────────────────────┤   │
│ │ Vol[60h]  TRACK 3 (55px alto)                                        │   │
│ │ Pan    ├──────────────────────────────────────────────────────────────┤   │
│ │        │  ...                                                         │   │
│ └────────┴──────────────────────────────────────────────────────────────┘   │
│ STATS BAR  (padding 4px 8px, border-top 1px)                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ TRANSPORT BAR  (márgenes 8,4,8,4)                           bg: #252536    │
│ [Render 32px] [████████ Progress 22px ████████] [Export WAV] [Export MP3]   │
│ Copyright 11px                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Resumen de dimensiones clave para el rediseño

| Elemento | Dimensión actual | Contexto |
|----------|-----------------|----------|
| RangeSlider | **36px alto** fijo, label 125px, track desde 130px hasta w−60px, handle ⌀14px | 6 instancias en Composition |
| LabeledSlider | label 120px + slider flexible + valor 70px | Varios en Composition y Effects |
| DensityCurvePreview | **70px alto**, min 180px ancho | 1 instancia en Composition |
| MixerStrip | **80px ancho**, M/S 30×22, Vol 60px alto | 1 por track |
| Track lane | **55px alto**, evento 49px | N tracks |
| Ruler | **20px alto** | 1 en Timeline |
| Waveform | **35px alto** en source, 30–60px genérico | 1 por source |
| Botones acción | **36px alto** (Compose, Reroll), **32px** (Render) | 3 totales |
| Botón estándar | **24px alto** mín, padding 6×14 | Global |
| GroupBox | radius 6px, margin-top 10px, padding-top 18px | Contenedores de secciones |
| Splitter handles | **3px** | Arrastrables |
