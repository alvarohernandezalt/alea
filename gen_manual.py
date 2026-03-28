"""Generate comprehensive PDF manual for Aleatoric Composer — v2 fixed layout."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable,
)

# Page dimensions
PAGE_W, PAGE_H = A4  # 595.27 x 841.89 points
MARGIN = 18 * mm
USABLE_W = PAGE_W - 2 * MARGIN  # ~487 points

# Colors
ACCENT = HexColor("#7c6ff0")
ACCENT2 = HexColor("#4ecdc4")
TEXT_P = HexColor("#2a2a3e")
TEXT_S = HexColor("#555577")
CORAL = HexColor("#ff6b6b")
LIGHT_BG = HexColor("#f0f0f5")
BORDER = HexColor("#ccccdd")
BG_DARK = HexColor("#1e1e2e")

# Styles
s_title = ParagraphStyle("T", fontSize=22, textColor=ACCENT, fontName="Helvetica-Bold",
                          spaceAfter=6, alignment=TA_CENTER)
s_subtitle = ParagraphStyle("ST", fontSize=11, textColor=TEXT_S, fontName="Helvetica",
                             spaceAfter=20, alignment=TA_CENTER)
s_h1 = ParagraphStyle("H1", fontSize=15, textColor=ACCENT, fontName="Helvetica-Bold",
                        spaceBefore=16, spaceAfter=6)
s_h2 = ParagraphStyle("H2", fontSize=12, textColor=TEXT_P, fontName="Helvetica-Bold",
                        spaceBefore=12, spaceAfter=4)
s_h3 = ParagraphStyle("H3", fontSize=10, textColor=ACCENT2, fontName="Helvetica-Bold",
                        spaceBefore=8, spaceAfter=3)
s_body = ParagraphStyle("B", fontSize=9, textColor=TEXT_P, fontName="Helvetica",
                          spaceAfter=4, leading=12, alignment=TA_JUSTIFY)
s_bullet = ParagraphStyle("BL", fontSize=9, textColor=TEXT_P, fontName="Helvetica",
                            spaceAfter=2, leading=12, leftIndent=14, bulletIndent=4)
s_note = ParagraphStyle("N", fontSize=8.5, textColor=TEXT_S, fontName="Helvetica-Oblique",
                          spaceAfter=5, leading=11, leftIndent=10)
# Style for wrapping text inside table cells
s_cell = ParagraphStyle("C", fontSize=8, textColor=TEXT_P, fontName="Helvetica", leading=10)
s_cell_bold = ParagraphStyle("CB", fontSize=8, textColor=TEXT_P, fontName="Helvetica-Bold", leading=10)
s_cell_code = ParagraphStyle("CC", fontSize=7.5, textColor=TEXT_P, fontName="Courier", leading=10)
s_cell_header = ParagraphStyle("CH", fontSize=8, textColor=white, fontName="Helvetica-Bold", leading=10)


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6, spaceBefore=3)


def P(text, style=s_body):
    return Paragraph(text, style)


def section(num, title):
    return P(f"{num}. {title}", s_h1)


def make_table(headers, rows, col_pcts, header_bg=ACCENT):
    """Create table with Paragraph-wrapped cells. col_pcts = list of percentages summing to 100."""
    col_widths = [USABLE_W * p / 100.0 for p in col_pcts]

    # Wrap header cells
    h_cells = [Paragraph(h, s_cell_header) for h in headers]

    # Wrap data cells
    wrapped_rows = []
    for row in rows:
        wrapped = []
        for i, cell in enumerate(row):
            if i == 0:
                wrapped.append(Paragraph(str(cell), s_cell_code))
            else:
                wrapped.append(Paragraph(str(cell), s_cell))
        wrapped_rows.append(wrapped)

    data = [h_cells] + wrapped_rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_BG, white]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def param_table(rows):
    """Parameter table: name, type, range, default, description."""
    return make_table(
        ["Parametro", "Tipo", "Rango", "Default", "Descripcion"],
        rows, [17, 10, 14, 10, 49]
    )


def build_pdf():
    outpath = r"C:\Users\AdminLocal\Documents\GitHub\2026fundamental\Manual_AleatoricComposer_Completo.pdf"
    doc = SimpleDocTemplate(outpath, pagesize=A4,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=16 * mm, bottomMargin=16 * mm)
    S = []  # story

    # ===== COVER =====
    S.append(Spacer(1, 50))
    S.append(P("ALEATORIC COMPOSER", s_title))
    S.append(P("para la Escuela SUR (beta)", ParagraphStyle(
        "s", fontSize=14, textColor=ACCENT2, fontName="Helvetica", spaceAfter=10, alignment=TA_CENTER)))
    S.append(Spacer(1, 8))
    S.append(hr())
    S.append(P("Manual de Referencia Completo<br/>Todas las pestanas, controles y funcionalidades", s_subtitle))
    S.append(P("Version 0.1.0-beta  |  Marzo 2026", ParagraphStyle(
        "v", fontSize=10, textColor=TEXT_S, alignment=TA_CENTER, spaceAfter=6)))
    S.append(P("Alvaro Hernandez Altozano", ParagraphStyle(
        "a", fontSize=11, textColor=TEXT_P, alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=30)))

    # TOC
    S.append(Spacer(1, 15))
    S.append(P("INDICE DE CONTENIDOS", s_h2))
    S.append(hr())
    toc = [
        "1. Vision General de la Aplicacion",
        "2. Panel SOURCES (Panel Izquierdo)",
        "3. Tab COMPOSITION (Pestana Composicion)",
        "4. Tab EFFECTS PALETTE (Pestana Efectos)",
        "5. Tab XENAKIS (Tecnicas Estocasticas) [NUEVO]",
        "    5.1 Sub-tab Distribuciones de Probabilidad",
        "    5.2 Sub-tab Cadenas de Markov",
        "    5.3 Sub-tab Cribas (Sieves)",
        "    5.4 Sub-tab Random Walks",
        "6. TIMELINE (Panel Inferior)",
        "7. Barra de Transporte",
        "8. Estrategias de Composicion",
        "9. Catalogo Completo de Efectos",
        "10. Arquitectura Interna",
        "11. Flujo de Trabajo del Usuario",
    ]
    for t in toc:
        indent = 16 if t.startswith("    ") else 0
        S.append(P(t.strip(), ParagraphStyle("toc", fontSize=9.5, textColor=TEXT_P,
                                              leftIndent=indent, spaceAfter=2, leading=13)))
    S.append(PageBreak())

    # ===== 1. VISION GENERAL =====
    S.append(section("1", "VISION GENERAL DE LA APLICACION"))
    S.append(hr())
    S.append(P("Aleatoric Composer es una aplicacion de escritorio para composicion semi-aleatoria "
               "de audio. Permite cargar archivos de audio, configurar parametros de aleatoriedad, "
               "y generar composiciones multipista donde los eventos sonoros se distribuyen segun "
               "algoritmos estocasticos controlables."))
    S.append(Spacer(1, 4))
    S.append(P("Layout de la Ventana Principal", s_h3))
    S.append(P("La ventana (1400x900px, redimensionable) se divide en 3 zonas:"))
    S.append(make_table(
        ["Zona", "Posicion", "Contenido"],
        [["Panel SOURCES", "Izquierda (280-400px fijo)", "Gestion de archivos de audio fuente"],
         ["Panel TABS", "Derecha (expandible)", "3 pestanas: Composition, Effects, Xenakis"],
         ["TIMELINE", "Inferior (splitter vertical)", "Vista multipista con eventos y mixer"],
         ["Transporte", "Fondo", "Render, progreso, export WAV/MP3"]],
        [18, 28, 54]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Las zonas se separan con QSplitters redimensionables.", s_note))
    S.append(PageBreak())

    # ===== 2. PANEL SOURCES =====
    S.append(section("2", "PANEL SOURCES (Panel Izquierdo)"))
    S.append(hr())
    S.append(P("Gestiona los archivos de audio que se usan como materia prima para la composicion."))
    S.append(P("Controles del Panel Sources", s_h3))
    S.append(make_table(
        ["Control", "Tipo Widget", "Funcion"],
        [["+ Add files", "QPushButton", "Abre dialogo para seleccionar archivos (.wav, .mp3, .flac, .ogg, .aiff)"],
         ["- Remove", "QPushButton", "Elimina el archivo seleccionado de la lista"],
         ["Lista fuentes", "QListWidget", "Muestra cada archivo con: nombre, duracion, canales, sample rate, mini waveform"],
         ["Drag & Drop", "Evento", "Arrastrar archivos desde el explorador directamente al panel"]],
        [18, 18, 64]
    ))
    S.append(Spacer(1, 5))
    S.append(P("Seccion SOURCE WEIGHTS", s_h3))
    S.append(P("Debajo de la lista aparece un slider horizontal por cada archivo cargado. "
               "Controla la probabilidad relativa de que ese archivo sea elegido como fuente."))
    S.append(param_table([
        ["Slider/fuente", "QSlider", "0 - 100", "100",
         "Peso relativo. 100 = probabilidad maxima, 0 = nunca se usa"],
    ]))
    S.append(Spacer(1, 4))
    S.append(P("Item de Fuente (por archivo)", s_h3))
    for item in ["Nombre del archivo (coloreado segun posicion en la lista)",
                 "Info: duracion (s), mono/stereo, sample rate (Hz)",
                 "Mini waveform dibujada con QPainter (WaveformWidget, 35px alto)"]:
        S.append(P(f"\u2022 {item}", s_bullet))
    S.append(PageBreak())

    # ===== 3. TAB COMPOSITION =====
    S.append(section("3", "TAB COMPOSITION (Pestana Composicion)"))
    S.append(hr())
    S.append(P("Primera pestana del panel derecho. Contiene todos los controles para configurar "
               "como se genera la composicion aleatoria. Es un QScrollArea con multiples secciones."))

    S.append(P("Seccion: General", s_h2))
    S.append(param_table([
        ["Strategy", "QComboBox", "4 opciones", "scatter",
         "Algoritmo: scatter, structured, layer, canon (ver seccion 8)"],
        ["Seed", "QSpinBox", "0 - 2^31", "42",
         "Semilla del generador aleatorio. Misma semilla = mismo resultado"],
        ["Random", "QPushButton", "N/A", "N/A",
         "Genera una semilla aleatoria nueva"],
        ["Duration (s)", "QDoubleSpinBox", "1.0 - 3600.0", "120.0",
         "Duracion total de la composicion en segundos"],
        ["Tracks", "QSpinBox", "1 - 16", "4",
         "Numero de pistas simultaneas"],
    ]))

    S.append(P("Seccion: Timing", s_h2))
    S.append(param_table([
        ["Event duration", "RangeSlider", "0.01 - 60.0 s", "0.5 - 30.0",
         "Rango de duracion de cada evento sonoro (doble slider min/max)"],
        ["Silence gap", "RangeSlider", "0.0 - 30.0 s", "0.0 - 5.0",
         "Rango de silencio entre eventos consecutivos en una pista"],
        ["Allow overlap", "QCheckBox", "Si / No", "Si",
         "Si esta activado, eventos pueden superponerse en el tiempo"],
    ]))

    S.append(P("Seccion: Dynamics", s_h2))
    S.append(param_table([
        ["Amplitude", "RangeSlider", "0.0 - 1.0", "0.3 - 1.0",
         "Rango de volumen de cada evento (0=silencio, 1=maximo)"],
        ["Pan", "RangeSlider", "-1.0 - 1.0", "-1.0 - 1.0",
         "Panorama estereo (-1=izquierda, 0=centro, 1=derecha)"],
        ["Fade in", "RangeSlider", "0.001 - 2.0 s", "0.01 - 0.5",
         "Rango de duracion del fade de entrada"],
        ["Fade out", "RangeSlider", "0.001 - 2.0 s", "0.01 - 1.0",
         "Rango de duracion del fade de salida"],
    ]))

    S.append(P("Seccion: Effects", s_h2))
    S.append(param_table([
        ["Probability", "LabeledSlider", "0.0 - 1.0", "0.7",
         "Probabilidad de que un evento tenga efectos (0.7 = 70%)"],
        ["Max per event", "QSpinBox", "1 - 10", "3",
         "Numero maximo de efectos encadenados por evento"],
    ]))

    S.append(P("Seccion: Structure", s_h2))
    S.append(param_table([
        ["Density curve", "QComboBox", "5 opciones", "constant",
         "Forma de la curva de densidad temporal"],
    ]))
    S.append(P("Opciones de Density Curve:", s_h3))
    S.append(make_table(
        ["Curva", "Descripcion"],
        [["constant", "Densidad uniforme a lo largo de toda la pieza"],
         ["crescendo", "Densidad aumenta linealmente de 0.3 a 2.0"],
         ["decrescendo", "Densidad disminuye linealmente de 2.0 a 0.3"],
         ["arc", "Sube y baja en arco sinusoidal (pico en el centro)"],
         ["wave", "Ondula con 4 ciclos sinusoidales"]],
        [18, 82]
    ))
    S.append(P("Un widget DensityCurvePreview (70px) dibuja la curva seleccionada.", s_note))

    S.append(P("Botones de Accion", s_h2))
    S.append(make_table(
        ["Boton", "Tipo", "Funcion"],
        [["Compose", "QPushButton (accent)", "Genera composicion con los parametros actuales"],
         ["Re-roll", "QPushButton", "Nueva variacion derivando una nueva semilla del RNG"]],
        [16, 24, 60]
    ))
    S.append(PageBreak())

    # ===== 4. TAB EFFECTS =====
    S.append(section("4", "TAB EFFECTS PALETTE (Pestana Efectos)"))
    S.append(hr())
    S.append(P("Segunda pestana. Permite explorar los 18 efectos disponibles y ver/ajustar "
               "sus parametros. Los efectos se aplican automaticamente durante la composicion."))
    S.append(P("Controles:", s_h3))
    for item in ["<b>Header:</b> Titulo 'EFFECTS PALETTE' + descripcion",
                 "<b>Effect selector:</b> QComboBox con los 18 efectos (alfabetico)",
                 "<b>Parameter area:</b> QScrollArea con sliders dinamicos segun efecto"]:
        S.append(P(f"\u2022 {item}", s_bullet))
    S.append(Spacer(1, 4))
    S.append(P("Lista de Efectos (18 total)", s_h3))
    S.append(make_table(
        ["Efecto", "Params", "Descripcion"],
        [["bitcrush", "1", "Reduccion de bits (lo-fi)"],
         ["chorus", "3", "Modulacion LFO (coro)"],
         ["compressor", "4", "Compresion de rango dinamico"],
         ["delay", "3", "Retardo con feedback"],
         ["distortion", "1", "Saturacion/overdrive"],
         ["gain", "1", "Ajuste de nivel"],
         ["granular", "7", "Sintesis granular custom (numpy/scipy)"],
         ["highpass_filter", "1", "Filtro paso alto"],
         ["limiter", "2", "Limitador de picos"],
         ["lowpass_filter", "1", "Filtro paso bajo"],
         ["phaser", "3", "Modulacion all-pass"],
         ["pitch_shift", "1", "Cambio de tono"],
         ["reverb", "5", "Reverberacion (Freeverb)"],
         ["spectral_freeze", "2", "Congela espectro en un drone"],
         ["spectral_gate", "1", "Gate espectral (umbral)"],
         ["spectral_shift", "1", "Desplaza bins de frecuencia"],
         ["spectral_smear", "2", "Blur espectral gaussiano"],
         ["time_stretch", "1", "Cambio velocidad sin alterar pitch"]],
        [20, 8, 72]
    ))
    S.append(PageBreak())

    # ===== 5. TAB XENAKIS =====
    S.append(section("5", "TAB XENAKIS — Tecnicas Estocasticas [NUEVO]"))
    S.append(hr())
    S.append(P("Tercera pestana. Implementa 4 tecnicas de composicion estocastica basadas en "
               "'Formalized Music' (1992) de Iannis Xenakis. Cada tecnica es un sub-tab."))
    S.append(P("Las tecnicas funcionan como <b>modificadores composables</b> que post-procesan "
               "la salida de cualquier estrategia. Se pueden combinar libremente."))
    S.append(Spacer(1, 3))
    S.append(param_table([
        ["Enable Xenakis", "QCheckBox", "Si / No", "No",
         "Master toggle. Activa/desactiva todas las tecnicas estocasticas"],
    ]))

    # 5.1 Distribuciones
    S.append(Spacer(1, 6))
    S.append(P("5.1 Sub-tab: DISTRIBUCIONES DE PROBABILIDAD", s_h2))
    S.append(hr())
    S.append(P("Cada parametro musical puede tener su propia distribucion estadistica, "
               "produciendo resultados con caracteristicas distintas."))

    S.append(P("Parametros con distribucion configurable:", s_h3))
    S.append(make_table(
        ["Parametro", "Afecta a", "Significado Musical"],
        [["timing", "Gap entre eventos", "Regularidad/irregularidad del ritmo"],
         ["amplitude", "Volumen de cada evento", "Distribucion de dinamicas"],
         ["pan", "Panorama estereo", "Distribucion espacial"],
         ["duration", "Duracion de cada evento", "Variedad de longitudes"]],
        [16, 26, 58]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Distribuciones disponibles:", s_h3))
    dists = [
        ["UNIFORM", "Probabilidad igual en todo el rango. Maximo desorden.", "low, high"],
        ["GAUSSIAN", "Valores concentrados alrededor de una media. Pocos extremos.", "mean, std"],
        ["EXPONENTIAL", "Valores cerca de 0 muy probables, valores grandes raros. Proceso Poisson.", "scale"],
        ["CAUCHY", "Como gaussiana pero con colas pesadas: outliers extremos mas frecuentes.", "loc, scale"],
        ["LINEAR", "Probabilidad crece o decrece linealmente. Sesgo hacia un extremo.", "ascending (bool)"],
        ["WEIBULL", "Forma flexible. shape&lt;1: muchos pequenos. shape&gt;1: pico desplazado.", "shape, scale"],
    ]
    S.append(make_table(
        ["Distribucion", "Descripcion", "Parametros"],
        dists, [16, 64, 20]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Controles GUI:", s_h3))
    S.append(param_table([
        ["Enable overrides", "QCheckBox", "Si / No", "No",
         "Activa distribuciones personalizadas por parametro"],
        ["Param selector", "QComboBox", "4 opciones", "timing",
         "Elige que parametro configurar"],
        ["Distribution", "QComboBox", "6 opciones", "uniform",
         "Elige la distribucion para el parametro seleccionado"],
        ["scale / std", "LabeledSlider", "0.01 - 10.0", "1.0",
         "Escala/dispersion (aparece segun distribucion)"],
        ["loc / mean", "LabeledSlider", "variable", "0.5",
         "Localizacion/media (aparece segun distribucion)"],
        ["shape", "LabeledSlider", "0.1 - 5.0", "1.0",
         "Forma (solo Weibull)"],
        ["ascending", "QCheckBox", "Si / No", "Si",
         "Direccion del sesgo (solo Linear)"],
    ]))
    S.append(PageBreak())

    # 5.2 Markov
    S.append(P("5.2 Sub-tab: CADENAS DE MARKOV", s_h2))
    S.append(hr())
    S.append(P("Matrices de transicion de Markov controlan secuencias de estados. "
               "El valor de un evento depende del anterior, creando trayectorias con 'memoria'."))
    S.append(P("Parametros controlables por Markov:", s_h3))
    S.append(make_table(
        ["Parametro", "Estados", "Mapeo a Valores"],
        [["Dinamicas", "pp, p, mp, mf, f, ff", "Cada estado = rango de amplitud"],
         ["Densidad", "sparse, medium, dense", "Cada estado = rango de gap entre eventos"],
         ["Registro", "low, mid, high", "Rangos de seleccion de fuente o pitch shift"],
         ["Efectos", "dry, light, heavy", "Probabilidad y cantidad de efectos"]],
        [15, 28, 57]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Presets de matrices de transicion:", s_h3))
    S.append(make_table(
        ["Preset", "Descripcion"],
        [["gradual", "Transiciones suaves, cambios pequenos entre estados adyacentes"],
         ["volatile", "Transiciones abruptas, saltos frecuentes entre extremos"],
         ["organic", "Largos periodos estables con cambios subitos (procesos naturales)"],
         ["dramatic", "Arco dramatico: construye tension, climax, descenso"]],
        [16, 84]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Controles GUI:", s_h3))
    S.append(param_table([
        ["Target param", "QComboBox", "4 opciones", "dynamics",
         "Parametro que controlara la cadena de Markov"],
        ["Preset", "QComboBox", "4 + custom", "gradual",
         "Matriz predefinida o personalizada"],
        ["Order", "QSpinBox", "1 - 3", "1",
         "Orden de la cadena (1=depende del actual, 2=de los 2 ultimos)"],
        ["Trans. table", "QTableWidget", "NxN editable", "preset",
         "Tabla con probabilidades de transicion (visible en modo custom)"],
        ["State mapping", "QTableWidget", "Nx2 editable", "preset",
         "Mapea cada estado a un rango de valores (min, max)"],
    ]))
    S.append(P("Cada fila de la tabla de transiciones debe sumar 1.0 (se normaliza automaticamente).", s_note))
    S.append(PageBreak())

    # 5.3 Cribas
    S.append(P("5.3 Sub-tab: CRIBAS (SIEVES)", s_h2))
    S.append(hr())
    S.append(P("Las cribas de Xenakis son estructuras de aritmetica modular. Definen que puntos "
               "de una rejilla temporal o de alturas estan 'permitidos'. Se basan en clases de residuo."))
    S.append(Spacer(1, 3))
    S.append(P("Concepto matematico:", s_h3))
    S.append(P("Clase de residuo <b>(M, R)</b> = {n : n mod M = R}.<br/>"
               "Ejemplo: (3, 0) = {0, 3, 6, 9, 12, ...} — cada 3er punto<br/>"
               "Ejemplo: (5, 1) = {1, 6, 11, 16, ...} — offset 1, cada 5 puntos<br/>"
               "Union: (3,0) | (5,1) = {0, 1, 3, 6, 9, 11, 12, ...}"))
    S.append(Spacer(1, 4))
    S.append(P("Dos tipos de criba:", s_h3))
    S.append(make_table(
        ["Tipo", "Unidad de Rejilla", "Efecto Musical"],
        [["Criba Ritmo", "Segundos (ej: 0.125s = semicorchea a 120 BPM)",
          "Eventos solo en puntos permitidos. Patrones ritmicos complejos no periodicos."],
         ["Criba Pitch", "Semitonos (1 semitono)",
          "Pitch shift solo en intervalos permitidos. Escalas microtonales o modos no estandar."]],
        [14, 36, 50]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Controles GUI:", s_h3))
    S.append(param_table([
        ["Seccion", "QLabel", "Ritmo / Pitch", "N/A",
         "Dos secciones: criba ritmica y criba de pitch"],
        ["Modulus", "QSpinBox", "2 - 24", "3",
         "Modulo de la clase de residuo"],
        ["Residue", "QSpinBox", "0 - (M-1)", "0",
         "Residuo (offset dentro del modulo)"],
        ["+ Add pair", "QPushButton", "N/A", "N/A",
         "Anade un par (modulo, residuo) a la criba"],
        ["- Remove", "QPushButton", "N/A", "N/A",
         "Elimina el par seleccionado"],
        ["Operation", "QComboBox", "union / intersect", "union",
         "Como combinar pares: union (permisiva) o interseccion (restrictiva)"],
        ["Grid unit", "QDoubleSpinBox", "0.01 - 2.0 s", "0.125",
         "Unidad de rejilla temporal (solo criba de ritmo)"],
        ["Preview", "Widget custom", "Visual", "N/A",
         "Vista step-sequencer con puntos activos de la criba"],
    ]))
    S.append(PageBreak())

    # 5.4 Random Walks
    S.append(P("5.4 Sub-tab: RANDOM WALKS (Paseos Aleatorios)", s_h2))
    S.append(hr())
    S.append(P("En vez de valores independientes, los Random Walks crean trayectorias correlacionadas: "
               "el valor de cada evento depende del anterior mas un paso aleatorio. Produce evoluciones "
               "suaves o movimientos erraticos pero conectados."))
    S.append(Spacer(1, 3))
    S.append(P("Parametros aplicables:", s_h3))
    S.append(make_table(
        ["Parametro", "Significado", "Efecto Musical"],
        [["amplitude", "Volumen de cada evento", "Dinamicas que evolucionan gradualmente (crescendo organico)"],
         ["pan", "Panorama estereo", "Movimiento espacial continuo (izquierda-derecha)"]],
        [16, 24, 60]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Modos de frontera (Boundary):", s_h3))
    S.append(make_table(
        ["Modo", "Descripcion"],
        [["reflecting", "El walk rebota en la frontera como una pelota. Siempre dentro del rango."],
         ["absorbing", "Se pega a la frontera hasta que un paso lo aleje. Periodos largos en extremos."],
         ["wrapping", "Envuelve de un extremo al otro. Saltos subitos entre extremos."]],
        [16, 84]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Controles GUI:", s_h3))
    S.append(param_table([
        ["Enable ampl.", "QCheckBox", "Si / No", "No",
         "Activa random walk para la amplitud"],
        ["Enable pan", "QCheckBox", "Si / No", "No",
         "Activa random walk para el panorama estereo"],
        ["Step distrib.", "QComboBox", "3 opciones", "gaussian",
         "Distribucion del paso: gaussian (suave), cauchy (saltos), uniform"],
        ["Step size", "LabeledSlider", "0.001 - 0.5", "0.1",
         "Tamano medio del paso. Pequeno=lento, Grande=rapido"],
        ["Boundary", "QRadioButton x3", "3 opciones", "reflecting",
         "Comportamiento al llegar a los limites"],
        ["Preview", "Widget custom", "Grafico", "N/A",
         "Canvas con trayectoria de ejemplo del walk configurado"],
    ]))
    S.append(PageBreak())

    # ===== 6. TIMELINE =====
    S.append(section("6", "TIMELINE (Panel Inferior)"))
    S.append(hr())
    S.append(P("Panel inferior que muestra la composicion generada de forma visual (QPainter)."))
    S.append(make_table(
        ["Componente", "Descripcion"],
        [["Eje temporal", "Horizontal, tiempo en segundos"],
         ["Carriles track", "Un carril horizontal por pista (~60px alto)"],
         ["Bloques evento", "Rectangulos coloreados por fuente, ancho proporcional a duracion"],
         ["Labels track", "Nombre de la pista a la izquierda"],
         ["Color/fuente", "Cada archivo fuente tiene color unico asignado automaticamente"]],
        [20, 80]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Interacciones:", s_h3))
    for i in ["Hover sobre evento: tooltip con info (source, duration, effects)",
              "Click sobre evento: selecciona y muestra detalles",
              "Los eventos NO se arrastran (composicion algoritmica)"]:
        S.append(P(f"\u2022 {i}", s_bullet))
    S.append(Spacer(1, 4))
    S.append(P("Colores de tracks:", s_h3))
    S.append(make_table(
        ["Track", "Color", "Nombre"],
        [["Track 1", "#4ecdc4", "Turquesa"],
         ["Track 2", "#ff6b6b", "Coral"],
         ["Track 3", "#ffd93d", "Amarillo"],
         ["Track 4", "#6bcb77", "Verde"],
         ["Track 5+", "Ciclo", "Se repiten ciclicamente"]],
        [20, 20, 60]
    ))

    # ===== 7. TRANSPORTE =====
    S.append(Spacer(1, 8))
    S.append(section("7", "BARRA DE TRANSPORTE"))
    S.append(hr())
    S.append(make_table(
        ["Control", "Tipo", "Funcion"],
        [["Render", "QPushButton (accent)", "Renderiza composicion a buffer (background thread)"],
         ["Progress", "QProgressBar", "Progreso del render (0-100%)"],
         ["Export WAV", "QPushButton", "Guarda como WAV 24-bit"],
         ["Export MP3", "QPushButton", "Guarda como MP3 320kbps"]],
        [16, 24, 60]
    ))
    S.append(P("El render se ejecuta en un QRunnable en background. "
               "Footer: '(c) Alvaro Hernandez Altozano 2026'.", s_note))
    S.append(PageBreak())

    # ===== 8. ESTRATEGIAS =====
    S.append(section("8", "ESTRATEGIAS DE COMPOSICION"))
    S.append(hr())

    S.append(P("8.1 SCATTER", s_h2))
    S.append(P("Dispersion aleatoria pura. Cada evento es independiente."))
    for i in ["Avanza linealmente, anadiendo gap + evento",
              "Gap ajustado por curva de densidad",
              "15% probabilidad de invertir cada evento",
              "Resultado: maximo caos, textura granular"]:
        S.append(P(f"\u2022 {i}", s_bullet))

    S.append(P("8.2 STRUCTURED", s_h2))
    S.append(P("Divide timeline en secciones con transiciones Markov."))
    S.append(make_table(
        ["Tipo Seccion", "Densidad", "Descripcion"],
        [["silence", "0.0", "Sin eventos. Pausa total."],
         ["sparse", "0.3", "Pocos eventos, texturas abiertas."],
         ["medium", "0.7", "Balance entre eventos y silencio."],
         ["dense", "1.0", "Muchos eventos superpuestos."],
         ["climax", "1.5", "Maxima densidad e intensidad."]],
        [18, 14, 68]
    ))

    S.append(P("8.3 LAYER", s_h2))
    S.append(P("Cada pista es una capa textural continua de una sola fuente. "
               "Segmentos con crossfade de 2s. Ideal para drones y paisajes."))

    S.append(P("8.4 CANON", s_h2))
    S.append(P("Track 1 genera secuencia base. Los demas la copian con offset temporal, "
               "variaciones de amplitud (60-100%), pan aleatorio y efectos diferentes. "
               "20% de probabilidad de invertir eventos en copias."))
    S.append(PageBreak())

    # ===== 9. CATALOGO EFECTOS =====
    S.append(section("9", "CATALOGO COMPLETO DE EFECTOS"))
    S.append(hr())

    S.append(P("9.1 Efectos Pedalboard (Spotify)", s_h2))

    effects = [
        ("REVERB", [
            ["room_size", "float", "0.0 - 1.0", "0.5", "Tamano de sala simulada"],
            ["damping", "float", "0.0 - 1.0", "0.5", "Absorcion de altas frecuencias"],
            ["wet_level", "float", "0.0 - 1.0", "0.33", "Nivel senal procesada"],
            ["dry_level", "float", "0.0 - 1.0", "0.4", "Nivel senal original"],
            ["width", "float", "0.0 - 1.0", "1.0", "Ancho estereo"],
        ]),
        ("DELAY", [
            ["delay_seconds", "float", "0.01 - 2.0", "0.5", "Tiempo de retardo"],
            ["feedback", "float", "0.0 - 1.0", "0.3", "Realimentacion"],
            ["mix", "float", "0.0 - 1.0", "0.5", "Mezcla wet/dry"],
        ]),
        ("PITCH SHIFT", [
            ["semitones", "float", "-24 - +24", "0.0", "Semitonos de transposicion"],
        ]),
        ("DISTORTION", [
            ["drive_db", "float", "0 - 100", "25.0", "Ganancia de saturacion (dB)"],
        ]),
        ("COMPRESSOR", [
            ["threshold_db", "float", "-60 - 0", "-20.0", "Umbral de compresion"],
            ["ratio", "float", "1.0 - 20.0", "4.0", "Ratio de compresion"],
            ["attack_ms", "float", "0.1 - 100", "1.0", "Ataque (ms)"],
            ["release_ms", "float", "10 - 1000", "100", "Release (ms)"],
        ]),
        ("GAIN", [
            ["gain_db", "float", "-60 - +30", "0.0", "Ajuste de nivel (dB)"],
        ]),
        ("LIMITER", [
            ["threshold_db", "float", "-60 - 0", "-1.0", "Techo de nivel"],
            ["release_ms", "float", "10 - 1000", "100", "Release (ms)"],
        ]),
        ("CHORUS", [
            ["rate_hz", "float", "0.1 - 10", "1.0", "Frecuencia LFO"],
            ["depth", "float", "0.0 - 1.0", "0.25", "Profundidad modulacion"],
            ["mix", "float", "0.0 - 1.0", "0.5", "Mezcla wet/dry"],
        ]),
        ("PHASER", [
            ["rate_hz", "float", "0.1 - 10", "1.0", "Frecuencia LFO"],
            ["depth", "float", "0.0 - 1.0", "0.5", "Profundidad"],
            ["mix", "float", "0.0 - 1.0", "0.5", "Mezcla wet/dry"],
        ]),
        ("HIGHPASS FILTER", [
            ["cutoff_hz", "float", "20 - 10000", "200", "Frecuencia de corte"],
        ]),
        ("LOWPASS FILTER", [
            ["cutoff_hz", "float", "20 - 20000", "5000", "Frecuencia de corte"],
        ]),
        ("BITCRUSH", [
            ["bit_depth", "float", "1 - 24", "8", "Bits de resolucion"],
        ]),
    ]
    for ename, eparams in effects:
        S.append(P(ename, s_h3))
        S.append(param_table(eparams))

    S.append(PageBreak())
    S.append(P("9.2 Efectos Custom (numpy/scipy/librosa)", s_h2))

    S.append(P("GRANULAR SYNTH", s_h3))
    S.append(P("Rompe audio en granos y los reensambla. Cada grano puede tener pitch, "
               "amplitud y posicion independientes."))
    S.append(param_table([
        ["grain_size_ms", "float", "5 - 500 ms", "50", "Tamano de cada grano"],
        ["grain_density", "float", "1 - 100 /s", "10", "Granos por segundo"],
        ["grain_scatter", "float", "0.0 - 1.0", "0.0", "Jitter aleatorio en onset"],
        ["position_start", "float", "0.0 - 1.0", "0.0", "Inicio region de lectura"],
        ["position_end", "float", "0.0 - 1.0", "1.0", "Fin region de lectura"],
        ["position_random", "float", "0.0 - 1.0", "0.0", "Variacion posicion lectura"],
        ["pitch_shift_st", "float", "-24 - +24", "0.0", "Pitch shift uniforme (st)"],
        ["pitch_random", "float", "0 - 12", "0.0", "Variacion pitch por grano"],
        ["amplitude_random", "float", "0.0 - 1.0", "0.0", "Variacion volumen/grano"],
        ["window_type", "enum", "4 opciones", "hann", "hann, hamming, blackman, triangular"],
        ["reverse_prob", "float", "0.0 - 1.0", "0.0", "Prob. invertir grano"],
        ["output_duration", "float", "null o s", "null", "Duracion fija salida"],
        ["seed", "int", "0 - 2^31", "42", "Semilla reproducibilidad"],
    ]))

    S.append(P("SPECTRAL FREEZE", s_h3))
    S.append(P("Congela espectro en un punto temporal, creando un drone sostenido (STFT)."))
    S.append(param_table([
        ["freeze_position", "float", "0.0 - 1.0", "0.5", "Punto temporal donde congelar"],
        ["output_duration", "float", "1.0 - 60.0", "10.0", "Duracion drone salida (s)"],
    ]))

    S.append(P("SPECTRAL SMEAR", s_h3))
    S.append(P("Blur gaussiano al espectrograma. Resultado: sonido lavado, sonador."))
    S.append(param_table([
        ["smear_amount", "float", "0 - 50", "5.0", "Sigma blur eje frecuencia"],
        ["time_smear", "float", "0 - 20", "0.0", "Sigma blur eje temporal"],
    ]))

    S.append(P("SPECTRAL GATE", s_h3))
    S.append(P("Pone a cero bins bajo umbral. Solo sobreviven frecuencias dominantes."))
    S.append(param_table([
        ["threshold", "float", "0.0 - 1.0", "0.1", "Umbral relativo al pico maximo"],
    ]))

    S.append(P("SPECTRAL SHIFT", s_h3))
    S.append(P("Desplaza bins de frecuencia. Transposiciones inarmonicas."))
    S.append(param_table([
        ["shift_bins", "int", "-200 - +200", "0", "Bins a desplazar (+agudo, -grave)"],
    ]))

    S.append(P("TIME STRETCH", s_h3))
    S.append(P("Cambia duracion sin alterar pitch (phase vocoder, librosa)."))
    S.append(param_table([
        ["rate", "float", "0.1 - 4.0", "1.0", "Factor velocidad (2.0=doble rapido)"],
    ]))
    S.append(PageBreak())

    # ===== 10. ARQUITECTURA =====
    S.append(section("10", "ARQUITECTURA INTERNA"))
    S.append(hr())
    S.append(P("Pipeline de datos:", s_h3))
    S.append(make_table(
        ["Paso", "Componente", "Entrada", "Salida"],
        [["1. Carga", "audio_io.load()", "Archivo audio", "AudioBuffer"],
         ["2. Config", "CompositionPanel", "Interaccion usuario", "Constraints"],
         ["3. Generacion", "Strategy.generate()", "Sources+Constraints+RNG", "Composition"],
         ["4. Modifiers", "Modifiers [NUEVO]", "Composition+Xenakis", "Composition mod."],
         ["5. Render", "Mixer.mix()", "Composition+Sources", "numpy stereo f32"],
         ["6. Export", "Exporter.export()", "numpy array", "WAV/MP3/FLAC"]],
        [12, 20, 30, 38]
    ))
    S.append(Spacer(1, 4))
    S.append(P("Modelo de datos: AudioEvent", s_h3))
    S.append(make_table(
        ["Campo", "Tipo", "Descripcion"],
        [["source_name", "str", "Nombre del archivo fuente"],
         ["source_start", "float", "Inicio segmento en fuente (s)"],
         ["source_end", "float", "Fin segmento en fuente (s)"],
         ["timeline_start", "float", "Posicion en timeline composicion"],
         ["track_index", "int", "Indice de pista"],
         ["amplitude", "float", "Volumen (0.0 - 1.0)"],
         ["pan", "float", "Panorama (-1.0 izq, 0 centro, 1.0 der)"],
         ["fade_in", "float", "Duracion fade entrada (s)"],
         ["fade_out", "float", "Duracion fade salida (s)"],
         ["effects_config", "list[dict]", "Efectos serializados [{type, params}]"],
         ["is_reversed", "bool", "Si se reproduce al reves"]],
        [18, 14, 68]
    ))
    S.append(Spacer(1, 4))
    S.append(P("RNG: ControlledRandom", s_h3))
    S.append(make_table(
        ["Metodo", "Descripcion"],
        [["uniform(low, high)", "Valor uniforme en rango"],
         ["gaussian(mean, std)", "Valor normal con clipping"],
         ["exponential(scale) [NUEVO]", "Valor exponencial (Poisson)"],
         ["cauchy(loc, scale) [NUEVO]", "Valor Cauchy (colas pesadas)"],
         ["poisson(lam) [NUEVO]", "Entero Poisson"],
         ["linear(low, high, asc) [NUEVO]", "Valor triangular sesgado"],
         ["weibull(shape, scale) [NUEVO]", "Valor Weibull"],
         ["sample(dist, low, high) [NUEVO]", "Dispatcher generico"],
         ["weighted_choice(items, wt)", "Eleccion ponderada"],
         ["markov_choice(state, mx)", "Siguiente estado Markov"],
         ["boolean(prob)", "Verdadero/falso con probabilidad"],
         ["fork()", "Crea RNG hijo independiente"]],
        [36, 64]
    ))
    S.append(PageBreak())

    # ===== 11. FLUJO DE TRABAJO =====
    S.append(section("11", "FLUJO DE TRABAJO DEL USUARIO"))
    S.append(hr())
    steps = [
        ("1", "Abrir la aplicacion", "La ventana se abre con todos los paneles vacios."),
        ("2", "Cargar archivos de audio",
         "Usar '+ Add files' o arrastrar desde explorador. Aparecen con waveform y color."),
        ("3", "Ajustar pesos por fuente",
         "Mover sliders de SOURCE WEIGHTS para controlar probabilidad de cada archivo."),
        ("4", "Configurar composicion (Tab Composition)",
         "Elegir estrategia, semilla, duracion, tracks. Ajustar timing, dinamicas, efectos, densidad."),
        ("5", "Configurar Xenakis (Tab Xenakis) [OPCIONAL]",
         "Activar distribuciones, Markov, cribas, y/o random walks segun resultado deseado."),
        ("6", "Componer",
         "Click 'Compose'. Se genera la composicion y aparece en el Timeline."),
        ("7", "Iterar",
         "Click 'Re-roll' para variaciones. Ajustar parametros y recomponer."),
        ("8", "Renderizar",
         "Click 'Render'. Audio se procesa en background (barra de progreso)."),
        ("9", "Exportar",
         "Click 'Export WAV' o 'Export MP3'. Elegir ubicacion y guardar."),
    ]
    for num, title, desc in steps:
        S.append(KeepTogether([
            P(f"<b>Paso {num}: {title}</b>", ParagraphStyle(
                "st", fontSize=10, textColor=ACCENT, fontName="Helvetica-Bold",
                spaceBefore=6, spaceAfter=2)),
            P(desc, ParagraphStyle(
                "sd", fontSize=9, textColor=TEXT_P, fontName="Helvetica",
                spaceAfter=3, leftIndent=14, leading=12)),
        ]))

    S.append(Spacer(1, 20))
    S.append(hr())
    S.append(P("Fin del Manual de Referencia", ParagraphStyle(
        "e", fontSize=10, textColor=TEXT_S, alignment=TA_CENTER, spaceAfter=4)))
    S.append(P("Aleatoric Composer para la Escuela SUR (beta) v0.1.0<br/>"
               "(c) Alvaro Hernandez Altozano 2026", ParagraphStyle(
        "ec", fontSize=9, textColor=TEXT_S, alignment=TA_CENTER)))

    doc.build(S)
    print(f"PDF generado: {outpath}")


if __name__ == "__main__":
    build_pdf()
