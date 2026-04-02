# 04 — Catálogo de Efectos CDP para Integración en v0.2

> CDP Release 8 (Trevor Wishart et al.) — Auditoría completa de efectos disponibles.
> Marca con **[X]** los que quieras integrar en Aleatoric Composer v0.2.
> Los marcados con **SPECTRAL** requieren paso previo `specanal` y posterior `pvoc`.
> Los marcados con **WAV** trabajan directamente sobre archivos de audio.

---

## Leyenda

| Símbolo | Significado |
|---------|-------------|
| WAV | Trabaja directamente sobre archivos .wav |
| SPECTRAL | Requiere análisis FFT previo (specanal→proceso→pvoc) |
| SYNTH | Genera audio desde cero (no necesita input) |
| MONO | Solo acepta entrada mono |
| TV | Parámetro time-variable (puede cambiar durante el proceso) |
| `[ ]` | Casilla para marcar si se integra en v0.2 |

---

## 1. REVERB Y DELAY

### 1.1 reverb — Reverberador multicanal
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| rgain | 0.0–1.0 | | Nivel del reverb denso |
| mix | 0.0–1.0 | | Balance dry/wet (1.0=dry, 0.0=wet) |
| rvbtime | segundos | | Tiempo de decaimiento a -60dB |
| absorb | 0.0–1.0 | | Absorción HF (simulación de aire) |
| lpfreq | Hz (0=off) | | Corte lowpass a la entrada del reverb |
| trtime | segundos | | Duración de la cola de reverb |
| -c N | 1–16 | | Canales de salida |
| -p N | ms | | Predelay forzado |
| -H N | Hz | | Highcut 6dB/oct en entrada |
| -L N | Hz | | Lowcut 12dB/oct en entrada |

---

### 1.2 rmverb — Reverb con simulación de sala
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| rmsize | 1=small, 2=medium, 3=large | | Tamaño de sala |
| rgain | 0.0–1.0 | | Nivel del reverb |
| mix | 0.0–1.0 | | Dry/wet |
| fback | 0.0–1.0 | | Feedback (controla decay) |
| absorb | Hz (0=off) | | Lowpass interno (2500 sala grande, 4200 pequeña) |
| lpfreq | Hz (0=off) | | Lowpass en entrada |
| trtime | segundos | | Cola de reverb |

---

### 1.3 newdelay — Delay basado en pitch con resonancia
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| midipitch | MIDI note | TV | Pitch que determina el delay time |
| mix | float | | Cantidad de señal retardada |
| feedback | float | | Resonancia (especialmente con delays cortos) |

---

### 1.4 sfecho — Echo simple con decaimiento
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| delay | segundos | TV | Tiempo entre repeticiones |
| attenuation | 0–1 | TV | Nivel de cada repetición |
| totaldur | segundos | | Duración máxima de salida |
| -r rand | float | TV | Randomización de tiempos de echo |
| -c cutoff | dB | | Nivel de corte (default -96dB) |

---

### 1.5 tapdelay — Delay multi-tap stereo con panning
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| tapgain | >0.0 | | Ganancia en salida de delay |
| feedback | -1.0–1.0 | | Feedback |
| mix | 0.0–<1.0 | | Proporción de señal original |
| trailtime | segundos | | Tiempo extra para que decaigan los delays |
| taps.txt | archivo | | Cada línea: tiempo amp [pan] — pan: -1 a +1 |

---

### 1.6 modify revecho — Reverb/echo/resonancia integrado
- **Tipo:** WAV
- **Integrar:** `[ ]`

**Modo 1 — Delay estándar:**

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| delay | ms | Tiempo de delay |
| mix | float | Señal retardada en mix (0=dry) |
| feedback | float | Resonancia |
| tail | segundos | Tiempo de decaimiento |
| -p prescale | float | Pre-atenuación |

**Modo 2 — Delay variable (LFO):**

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| delay, mix, feedback | (como Modo 1) | |
| lfomod | float | Profundidad del sweep |
| lfofreq | Hz (neg=random) | Frecuencia del sweep |
| lfophase | float | Fase inicial |
| lfodelay | segundos | Tiempo antes de que empiece el sweep |

**Modo 3 — Stadium echo:**

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| -g gain | float (dflt 0.645) | Ganancia de entrada |
| -r roll_off | float (dflt 1) | Pérdida de nivel |
| -s size | float | Multiplica tiempo entre ecos (dflt 0.1s) |
| -e count | int (dflt/max 1000) | Número de ecos |

---

### 1.7 fastconv — Convolución rápida
- **Tipo:** WAV
- **Integrar:** `[ ]`

> Convoluciona un archivo con un impulso (reverb por convolución, cross-synthesis, etc.)

---

### 1.8 dvdwind — Contracción temporal por read-skip
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| contraction | >1 | Factor de contracción |
| clipsize | ms | Duración de cada clip retenido |

---

## 2. FILTROS

### 2.1 filter fixed — Corte/boost en frecuencia fija
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Boost/cut por debajo de freq |
| 2 | Boost/cut por encima de freq |
| 3 | Boost/cut en banda centrada en freq |

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| freq | Hz | Frecuencia del filtro |
| boost/cut | dB | Cantidad de boost o corte |
| bwidth | Hz | Ancho de banda (solo Modo 3) |

---

### 2.2 filter variable — Filtro variable (LP/HP/BP/Notch)
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Notch (band reject) |
| 2 | Band-pass |
| 3 | Low-pass |
| 4 | High-pass |

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| acuity | 0.0001–1.0 | TV | Estrechez del filtro |
| gain | 0.001–10000 | | Ganancia de salida |
| frq | 0.1–sr/2 Hz | TV | Frecuencia del filtro |

---

### 2.3 filter lohi — Lowpass/Highpass fijo
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| attenuation | 0 a -96 dB | Reducción de ganancia |
| pass-band | Hz o MIDI | Último pitch que pasa |
| stop-band | Hz o MIDI | Primer pitch bloqueado |

---

### 2.4 filter bank — Banco de filtros con Q variable
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Serie armónica sobre lofrq |
| 2 | Armónicos alternos |
| 3 | Serie subarmónica bajo hifrq |
| 4 | Serie armónica con offset lineal |
| 5 | Intervalos iguales (por número de filtros) |
| 6 | Intervalos iguales (por semitonos) |

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| Q | 0.001–10000 | TV | Estrechez de filtros |
| gain | 0.001–10000 | | Ganancia global |
| lof | 0–sr/3 Hz | | Frecuencia baja |
| hif | lof+–sr/3 Hz | | Frecuencia alta |
| -s scat | 0–1 | | Dispersión aleatoria de frecuencias |
| -d | flag | | Doble filtrado |

---

### 2.5 filter userbank — Banco de filtros definido por usuario
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| datafile | archivo | | Pares pitch/amplitud |
| Q | 0.001–10000 | TV | Estrechez |
| gain | 0.001–10000 | | Ganancia |

---

### 2.6 filter varibank — Banco de filtros variable en el tiempo
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| data | archivo | TV | Líneas time-stamped de pares pitch/amp |
| Q | 0.001–10000 | TV | Estrechez |
| gain | 0.001–10000 | | Ganancia |
| -h hcnt | int | | Armónicos por pitch |
| -r rolloff | 0 a -96 dB | | Caída de nivel por armónico |

---

### 2.7 filter sweeping — Filtro con barrido de frecuencia
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Tipo |
|------|------|
| 1 | Notch | 2 | Band-pass | 3 | Low-pass | 4 | High-pass |

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| acuity | 0.0001–1.0 | TV | Estrechez |
| gain | 0.001–10000 | | Ganancia |
| lofrq | 0.1–sr/2 | TV | Freq mínima del sweep |
| hifrq | 0.1–sr/2 | TV | Freq máxima del sweep |
| sweepfrq | 0.0–200 Hz | TV | Velocidad de oscilación del sweep |
| -p phase | 0–1 | | Fase inicial |

---

### 2.8 filter iterated — Filtrado iterativo (más filtrado en cada repetición)
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| datafile | archivo | | Pares pitch/amplitud |
| Q | 0.001–10000 | | Estrechez |
| gain | 0.001–10000 | | Ganancia |
| delay | >0–32767 s | | Delay entre iteraciones |
| dur | >infile dur | | Duración mínima de salida |
| -r rand | 0–1 | | Randomización del delay |
| -p pshift | semitones | | Pitch shift máximo |
| -a ashift | 0–1 | | Reducción de amplitud máxima |
| -e | flag | | Decaimiento exponencial |

---

### 2.9 filter phasing — Phaser
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Allpass (phase-shifted) |
| 2 | Phasing clásico |

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| gain | -1.0–1.0 | | Ganancia (Modo 2: 1.0=cancelación total) |
| delay | >0.0 ms | TV | Delay del phaser |

---

### 2.10 synfilt — Síntesis de ruido filtrado
- **Tipo:** SYNTH
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| data | archivo | Datos de filtro (varibank format) |
| dur | segundos | Duración |
| srate | int | Sample rate |
| Q | 0.001–10000 | Estrechez |
| gain | float | Ganancia |
| hcnt | int | Armónicos por pitch |
| rolloff | 0 a -96 dB | Caída por armónico |

---

## 3. DISTORSIÓN

### 3.1 distort — Suite de distorsión por wavecycles (21 sub-modos)
- **Tipo:** WAV / MONO
- **Integrar:** `[ ]`

#### Sub-modos principales:

| Sub-modo | Descripción | Parámetros clave |
|----------|-------------|------------------|
| **fractal** | Copia miniatura del wavecycle sobre sí mismo | `scaling` 2–sr/2 (TV), `loudness` (TV) |
| **harmonic** | Distorsión armónica superponiendo armónicos | `harmonics-file` (pares armónico/amp) |
| **multiply** | Multiplica frecuencia de wavecycles | `N` 2–16 |
| **divide** | Divide frecuencia de wavecycles | `N` 2–16 |
| **overload** | Clip con ruido o waveform | `clip_level` 0–1 (TV), `depth` 0–1 (TV), `freq` Hz (TV) |
| **reform** | Cambia forma del wavecycle | 8 modos: square, triangle, inverted, clicks, sinusoid, exaggerated |
| **pitch** | Transpone wavecycles aleatoriamente | `octvary` 0–8 oct (TV), `cyclelen` >1 (TV) |
| **envel** | Envelope sobre grupos de wavecycles | `cyclecnt` (TV), 4 modos: rising/falling/trough/user |
| **repeat** | Timestretch repitiendo wavecycles | `multiplier` int (TV) |
| **reverse** | Invierte wavecycles en grupos | `cyclecnt` (TV) |
| **shuffle** | Permuta wavecycles (domain-image) | `domain-image` string, `cyclecnt` (TV) |
| **delete** | Contrae tiempo eliminando wavecycles | `cyclecnt` (TV), 3 modos |
| **filter** | Elimina wavecycles por frecuencia | `freq` Hz (TV), 3 modos |
| **interpolate** | Timestretch con interpolación | `multiplier` (TV) |
| **telescope** | Telescopia N wavecycles en 1 | `cyclecnt` (TV) |
| **omit** | Omite A de cada B wavecycles | `A` (TV), `B` |
| **replace** | Reemplaza grupo por el más fuerte | `cyclecnt` (TV) |
| **average** | Promedia waveshape sobre N ciclos | `cyclecnt` >1 |
| **pulsed** | Tren de impulsos sobre la fuente | `env`, `frq` 0.1–50 Hz, `frand` 0–12 st, `trand` 0–1, `arand` 0–1 |
| **interact** | Interacción temporal de 2 archivos | 2 modos: interleave / impose wavelengths |

---

### 3.2 distcut — Corta en elementos con envelope descendente
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| cyclecnt | int | Wavesets por archivo de salida |
| exp | float | Forma del decay (1=lineal, >1=rápido, <1=lento) |
| -c limit | dB | Nivel mínimo aceptable |

---

### 3.3 distmark — Interpolación entre grupos de wavesets en puntos marcados
- **Tipo:** WAV / MONO
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| marklist | archivo | | Lista de tiempos |
| unitlen | ms | TV | Tamaño aprox del grupo de wavesets |
| -s tstretch | float | | Estira distancias entre marcas |
| -r rand | 0–1 | | Randomiza duraciones |

---

### 3.4 clip — Recorte de señal
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Clip a nivel especificado |
| 2 | Clip de half-waveforms a fracción especificada |

---

### 3.5 constrict — Acorta secciones de silencio
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| constriction | 0–200% | Porcentaje de eliminación de silencios |

---

### 3.6 crumble — Desintegración multicanal progresiva
- **Tipo:** WAV / MONO → 8 o 16 canales
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| stt | segundos | | Inicio del crumbling |
| dur1, dur2, dur3 | segundos | | Duraciones de cada fase de split |
| size | segundos | TV | Tamaño promedio de segmentos |
| rand | 0–1 | TV | Randomización del tamaño |
| pscat | semitonos | TV | Variación de pitch |

---

### 3.7 bounce — Rebotes con aceleración y decaimiento
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| count | int | Número de rebotes |
| startgap | 0.04–10 s | Gap entre fuente y primer rebote |
| shorten | float | Reducción del gap entre rebotes |
| endlevel | 0–1 | Nivel del último rebote |
| ewarp | float | >1=decresc rápido al inicio, <1=lento |
| -s min | float | Shrink elementos; valor=duración mínima |

---

### 3.8 splinter — Astillas repetidas y encogidas de wavesets
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| target | segundos | Tiempo en la fuente |
| wcnt | int | Wavesets en el grupo de astillas |
| shrcnt | int | Repeticiones con encogimiento |
| ocnt | int | Astillas adicionales después del shrink |
| p1, p2 | Hz | Velocidad de pulso origen/destino |
| -f frq | Hz | Frecuencia de astillas maximamente encogidas |

---

### 3.9 shrink — Repite acortando progresivamente
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Encoge desde el final |
| 2 | Encoge alrededor del centro |
| 3 | Encoge desde el inicio |
| 4 | Encoge alrededor de un tiempo dado |
| 5-6 | Encoge alrededor de picos encontrados/especificados |

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| shrinkage | float | Factor de acortamiento por repetición |
| gap | float | Gap inicial entre eventos |
| contract | float | Acortamiento de gaps (1.0=regular) |
| dur | float | Duración mínima de salida |

---

### 3.10 quirk — Distorsión por potencia de muestras
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| powfac | 0.01–100 | <1 exagera contorno, >1 suaviza |

---

### 3.11 scramble — Reordena wavesets
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Orden aleatorio |
| 2 | Permutación (todos antes de repetir) |
| 3-4 | Por tamaño (pitch descendente/ascendente) |
| 9-10 | Por nivel (crescendo/decrescendo) |

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| -c cnt | 1–256 | | Wavesets por grupo |
| -t trns | 0–12 st | TV | Transposición aleatoria |
| -a atten | 0–1 | TV | Atenuación aleatoria |
| seed | 0–256 | | Seed |

---

## 4. GRANULAR

### 4.1 grain — Suite de operaciones sobre granos (16 sub-modos)
- **Tipo:** WAV
- **Integrar:** `[ ]`

**Parámetros comunes a casi todos los sub-modos:**

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| -l gate | 0–1 | TV | Nivel mínimo para detectar grano |
| -h minhole | ≥0.032 s | | Duración mínima de silencio entre granos |
| -b len | float | | Tiempo máximo entre granos |
| -t winsize | ms | | Window para tracking de nivel |

#### Sub-modos principales:

| Sub-modo | Descripción | Parámetros extra |
|----------|-------------|------------------|
| **omit** | Omite proporción de granos | `keep` (TV), `out_of` |
| **repitch** | Transpone granos por lista de semitonos | `transpfile` (±48 st max) |
| **timewarp** | Stretch/shrink sin estirar granos | `ratio` 0.001–1000 (TV) |
| **duplicate** | Duplica granos | `N` repeticiones (TV) |
| **rerhythm** | Cambia ritmo con multiplicadores | `multfile` (0.001–1000) |
| **reverse** | Invierte orden de granos | (sin params extra) |
| **reposition** | Reposiciona granos a tiempos dados | `timefile`, `offset` |
| **reorder** | Reordena por patrón codificado | `code` (ej: "adb:c") |
| **remotif** | Cambia pitch Y ritmo simultáneamente | `transpmultfile` |
| **r_extend** | Extiende sonidos iterativos (ej: "rrr") | `te`, `pr`, `rep`, `get`, `asc` 0–1, `psc` 0–24 st |
| **grev** | Manipula granos por envelope troughs | 7 modos: reverse, repeat, delete, omit, timestretch, get, put |
| **noise_extend** | Extiende componente de ruido | `duration`, `minfrq` Hz, `mindur` ms, `maxdur` s |
| **align** | Sincroniza granos de 2 archivos | 2 archivos + `offset` |

---

### 4.2 grainex extend — Extiende zona de granos
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| wsiz | ms | Window size para encontrar granos |
| trof | >0–<1 | Altura aceptable de troughs |
| plus | segundos | Duración añadida |
| stt, end | segundos | Inicio/fin del material granular |

---

### 4.3 grnmill — Granulador completo
- **Tipo:** WAV
- **Integrar:** `[ ]`

> Granulación completa con control de tamaño de grano, densidad, pitch, amplitud y espacialización. Documentación detallada en GRNMILL.HLP.

---

### 4.4 hover — Lectura zigzag a frecuencia dada
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| frq | Hz | TV | Frecuencia de zigzag (determina ancho) |
| loc | segundos | TV | Posición de lectura en la fuente |
| frqrand | 0–1 | TV | Variación aleatoria de frecuencia |
| locrand | 0–1 | TV | Variación aleatoria de posición |
| splice | ms | | Splices en extremos del zigzag |
| dur | segundos | | Duración total de salida |

---

### 4.5 hover2 — Zigzag desde zero-crossings (waveforms simétricas)
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| frq | Hz | TV | Frecuencia de lectura |
| loc | segundos | TV | Posición de lectura |
| frqrand | 0–1 | TV | Variación de frecuencia |
| locrand | 0–1 | TV | Variación de posición |
| dur | segundos | | Duración de salida |

---

### 4.6 stutter — Corta en sílabas y reordena
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| datafile | archivo | | Tiempos de corte (min 0.016s) |
| dur | segundos | | Duración de salida |
| segjoins | 1–8 | | Elementos consecutivos que se unen |
| silprop | 0–1 | | Proporción de silencios insertados |
| silmin, silmax | segundos | | Rango de duración de silencios |
| seed | int | | Seed |
| -t trans | semitonos | | Transposición aleatoria |
| -a atten | 0–1 | | Atenuación aleatoria |
| -b bias | -1–1 | | Sesgo del tamaño de segmentos |

---

### 4.7 packet — Aísla o genera paquetes de onda
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| times | segundos o archivo | Tiempo(s) de extracción |
| narrowing | 0–1000 | Estrechamiento del envelope del paquete |
| centring | -1–1 | Centro del pico (-1=inicio, 0=centro, 1=final) |

---

### 4.8 wrappage — Reconstitución granular multicanal
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| outchans | int | | Canales de salida |
| centre | 0–outchans | TV | Posición central en el espacio |
| spread | float | TV | Ancho de espacialización |
| veloc | ≥0 | TV | Velocidad de avance (inverso de timestretch) |
| dens | >0 | TV | Solapamiento de granos (<1=silencios) |
| gsize | ms (>2×splice) | TV | Tamaño de grano (dflt 50) |
| pshift | ±semitonos | TV | Pitch shift |
| amp | 0–1 | TV | Ganancia de granos |
| bsplice, esplice | ms | TV | Splices de inicio/fin de grano |
| range | ms | TV | Rango de búsqueda del siguiente grano |
| jitter | 0–1 | TV | Randomización de posición (dflt 0.5) |

> Todos los parámetros tienen versión `h*` (high range) para randomización entre valor y hvalor.

---

### 4.9 modify brassage — Brassage granular (Wishart)
- **Tipo:** WAV
- **Integrar:** `[ ]`

> El brassage de Wishart: reconstitución granular con control completo de velocidad, pitch, densidad, tamaño de grano, scatter y espacialización. Accesible vía `modify brassage`.

---

## 5. TIEMPO Y PITCH

### 5.1 modify speed — Cambio de velocidad/pitch
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción | Parámetros |
|------|-------------|------------|
| 1 | Por multiplicador de velocidad | `speed` (TV) |
| 2 | Por semitonos | `semitone-transpos` (TV) |
| 5 | Aceleración/deceleración | `accel`, `goaltime`, `starttime` |
| 6 | Añadir vibrato | `vibrate` Hz (TV), `vibdepth` st (TV) |

---

### 5.2 strans multi — Cambio de velocidad/pitch multicanal
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción | Parámetros |
|------|-------------|------------|
| 1 | Multiplicador de velocidad | `speed` (TV) |
| 2 | Semitonos | `semitone-transpos` (TV) |
| 3 | Aceleración | `accel`, `goaltime` |
| 4 | Vibrato | `vibfrq` Hz (TV), `vibdepth` st (TV) |

---

### 5.3 retime — Ajuste rítmico de eventos
- **Tipo:** WAV
- **Integrar:** `[ ]`

> 14 modos para ajustar ritmo: regular pulse, timestretch eventos, speed factor, posicionar en beats/tiempos, repetir a tempo, eliminar en patrón, ajustar niveles, encontrar picos. Ideal para trabajo rítmico.

---

### 5.4 psow — Operaciones sobre granos pitch-síncronos (FOFs)
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Sub-modo | Descripción |
|----------|-------------|
| stretch | Stretch por repetición de FOFs |
| dupl | Duplicar FOFs |
| delete | Eliminar FOFs |
| strtrans | Stretch con transposición |
| grab | Capturar FOFs |
| sustain | Sostener FOFs |
| chop | Cortar FOFs |
| interp | Interpolar entre FOFs |
| synth | Síntesis desde FOFs |
| impose | Imponer FOFs |
| space | Espacializar FOFs |
| reinforce | Reforzar FOFs |

---

### 5.5 tweet — Reemplaza FOFs vocales por tweets/ruido
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Reemplaza FOFs con tweets (freq variable) |
| 2 | Reemplaza FOFs con tweets (freq fija) |
| 3 | Reemplaza FOFs con ruido |

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| pitchdata | archivo | Datos de pitch (breakpoint time/freq) |
| minlevel | dB | FOFs por debajo de este nivel se rechazan |
| pkcnt | 1–200 | Picos en el impulso (Modo 1) |
| frq | 1–200 | Frecuencia de picos (Modo 2) |
| chirp | 0–30 | Glissando del impulso |

---

## 6. SPECTRAL (requieren specanal→proceso→pvoc)

### 6.1 blur — 10 operaciones de difuminado espectral
- **Tipo:** SPECTRAL
- **Integrar:** `[ ]`

| Sub-modo | Descripción | Parámetros clave |
|----------|-------------|------------------|
| **avrg** | Promedia energía sobre N canales adyacentes | `N` impar (TV) |
| **blur** | Promedia temporalmente el espectro | `blurring` int (TV) |
| **suppress** | Suprime los N parciales más fuertes | `N` int (TV) |
| **chorus** | Chorusing randomizando amps/freqs | `aspread` 1–1028, `fspread` 1–4, 7 modos |
| **drunk** | Drunken walk por ventanas de análisis | `range`, `starttime`, `duration` |
| **shuffle** | Permuta ventanas (domain-image) | `domain-image` string, `grpsize` |
| **weave** | Teje entre ventanas con secuencia | `weavfile` archivo |
| **noise** | Añade ruido al espectro | `noise` 0–1 (TV) |
| **scatter** | Thins espectro manteniendo bloques | `keep` (TV), `-b blocksize` |
| **spread** | Expande picos introduciendo ruido | `-f/-p N`, `spread` 0–1 |

---

### 6.2 morph — Morphing entre espectros
- **Tipo:** SPECTRAL (2 inputs)
- **Integrar:** `[ ]`

> Sub-modos: glide, bridge, morph

---

### 6.3 newmorph — Nuevos tipos de morphing espectral
- **Tipo:** SPECTRAL (2 inputs)
- **Integrar:** `[ ]`

---

### 6.4 focus — Operaciones de enfoque espectral
- **Tipo:** SPECTRAL
- **Integrar:** `[ ]`

> Sub-modos: accu, exag, focus, fold, freeze, hold, step

---

### 6.5 hilite — Resaltado espectral
- **Tipo:** SPECTRAL
- **Integrar:** `[ ]`

> Sub-modos: filter, greq, band, arpeg, pluck, trace, bltr, vowels

---

### 6.6 specfnu — 23 modos de manipulación de formantes
- **Tipo:** SPECTRAL
- **Integrar:** `[ ]`

| Modos destacados | Descripción |
|------------------|-------------|
| 1 | Estrechar formantes |
| 2 | Comprimir espectro alrededor de un formante |
| 3 | Invertir formantes (picos↔valles) |
| 4 | Rotar formantes |
| 5 | Negativo espectral |
| 10 | Arpegiar parciales bajo formantes |
| 11 | Octave-shift bajo formantes |
| 12 | Transponer bajo formantes |
| 14 | Re-espaciar parciales bajo formantes |
| 18 | Randomizar pitch bajo formantes |
| 23 | Sine speech (un seno por formante) |

---

### 6.7 specfold — Plegar/invertir/randomizar espectro
- **Tipo:** SPECTRAL
- **Integrar:** `[ ]`

| Modo | Descripción | Parámetros |
|------|-------------|------------|
| 1 | Fold spectrum | `stt`, `len` (≥4, par), `cnt` |
| 2 | Invert spectrum | `stt`, `len` |
| 3 | Randomise spectrum | `stt`, `len`, `seed` |

---

### 6.8 specsphinx — Cross-spectral (imposición/multiplicación)
- **Tipo:** SPECTRAL (2 inputs)
- **Integrar:** `[ ]`

| Modo | Descripción | Parámetros |
|------|-------------|------------|
| 1 | Amps de file2 sobre freqs de file1 | `-a` ampbalance 0–1, `-f` frqbalance 0–1 |
| 2 | Multiplicar espectros | `-b` bias, `-g` gain |

---

### 6.9 spectstr — Time-stretch espectral anti-artefactos
- **Tipo:** SPECTRAL
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| timestretch | float (TV) | Factor de estiramiento |
| d-ratio | float | Proporción de canales para decoherencia |
| di-rand | float | Randomización de freq de canales decoherentes |

---

### 6.10 spectwin — Interpolación entre 2 espectros por envolventes
- **Tipo:** SPECTRAL (2 inputs)
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| -f frqint | 0–1 | Dominancia de freqs de file2 |
| -e envint | 0–1 | Dominancia de envelope de file2 |
| -d dupl | int | Duplicar sonido-1 a pitches superiores |
| -s step | semitonos | Paso de pitch por duplicación |

---

### 6.11 stretch — Stretch espectral y temporal
- **Tipo:** SPECTRAL
- **Integrar:** `[ ]`

| Sub-modo | Descripción | Parámetros |
|----------|-------------|------------|
| spectrum 1 | Stretch freqs por encima de frq_divide | `frq_divide`, `maxstretch`, `exponent` >0, `-d` depth 0–1 |
| spectrum 2 | Stretch freqs por debajo de frq_divide | (igual) |
| time 1 | Time-stretch | `timestretch` (TV) |

---

### 6.12 glisten — Partición aleatoria del espectro
- **Tipo:** SPECTRAL
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| grpdiv | int (divide chans exacto) | Conjuntos de partición |
| setdur | 1–1024 ventanas | Persistencia de cada set |
| -p pitchshift | 0–12 st | Pitch shift aleatorio por set |
| -d durrand | 0–1 | Randomización de duración |

---

## 7. MODULACIÓN Y TREMOLO

### 7.1 tremolo — Tremolo con narrowing
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| frq | 0–500 Hz | TV | Frecuencia del tremolo |
| depth | 0–1 | TV | Profundidad |
| gain | 0–1 | TV | Ganancia |
| fineness | ≥1 int | | Squeeze width (estrechamiento) |

---

### 7.2 tremenv — Tremolo post-peak del envelope
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| frq | 0–500 Hz | Frecuencia |
| depth | 0–1 | Profundidad |
| winsize | 1–40 ms | Window para extracción de envelope |
| fineness | ≥1 | Squeeze width |

---

### 7.3 flutter — Tremulación multicanal
- **Tipo:** WAV (multicanal)
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| chanseq | archivo | | Secuencia de sets de canales |
| freq | Hz | TV | Frecuencia de variación |
| depth | 0–16 | TV | Profundidad (1=cero en troughs, >1=picos más estrechos) |
| gain | 0–1 | | Ganancia |

---

### 7.4 phasor — Phasing por streams múltiples
- **Tipo:** WAV / MONO
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| streams | 2–8 | | Número de streams |
| phasfrq | float | TV | Frecuencia de paquetes de phase-shift |
| shift | 0–12 st | TV | Phase shift máximo |
| ochans | ≤streams | | Canales de salida |
| -o offset | 0–500 ms | | Offset temporal del stream más desplazado |

---

### 7.5 rotor — Sets de notas que crecen/encogen en rango y velocidad
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| cnt | 3–127 | Eventos por set |
| minp, maxp | MIDI 0–127 | Rango de pitch |
| step | 0–4 s | Timestep máximo entre eventos |
| prot | 4–256 | Notesets antes de volver al pitch original |
| trot | 4–256 | Speeds antes de volver |
| phas | 0–1 | Diferencia de fase entre prot y trot |
| dur | segundos | Duración de salida |

---

## 8. ENVELOPE

### 8.1 envel warp — 15 modos de deformación de envelope
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Normalise |
| 2 | Reverse envelope |
| 3 | Exaggerate dynamics |
| 4 | Attenuate |
| 5 | Lift low values |
| 6 | Timestretch envelope |
| 7 | Flatten |
| 8 | Gate |
| 9 | Invert |
| 10 | Limit |
| 11 | Corrugate |
| 12 | Expand |
| 13 | Trigger from ramp |
| 14 | Ceiling |
| 15 | Ducked |

---

### 8.2 envel impose — Imponer envelope
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Fuente del envelope |
|------|---------------------|
| 1 | Otro soundfile |
| 2 | Binary envelope file |
| 3 | Breakpoint file (0–1) |
| 4 | Breakpoint file (dB) |

---

### 8.3 envel replace — Reemplazar envelope
- **Tipo:** WAV
- **Integrar:** `[ ]`

> Mismos 4 modos que impose.

---

### 8.4 envel tremolo — Tremolo por modulación de envelope
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| frq | 0–500 Hz | TV | Frecuencia |
| depth | 0–1 | TV | Profundidad (dflt 0.25) |
| gain | 0–1 | TV | Ganancia |

---

### 8.5 envel attack — Enfatizar ataque
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| gain | float | Amplificación del punto de ataque |
| onset | 5–32767 ms | Duración del onset del ataque |
| decay | 5 ms a <duración | Duración del decay del ataque |

---

### 8.6 envel dovetail — Fade-in/out
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| infadedur | float | Duración del fade-in |
| outfadedur | float | Duración del fade-out |
| intype, outtype | 0=lineal, 1=exponencial | Tipo de curva |

---

### 8.7 envel pluck — Ataque de pluck
- **Tipo:** WAV / MONO
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| startsamp | int | Muestra donde termina el pluck |
| wavelen | int | Longitud de onda del pluck |
| -a atkcycles | 2–32767 | Wavecycles en el ataque |
| -d decayrate | 1–64 | Velocidad de decaimiento |

---

### 8.8 envcut — Cortar con envelope descendente
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| envlen | segundos | Duración de cada corte |
| attack | ms | Duración del ataque |
| exp | float | 1=lineal, >1=rápido, <1=lento |

---

### 8.9 envspeak — Procesamiento de sílabas (25 modos)
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modos destacados | Descripción |
|------------------|-------------|
| 1 | Repetir cada sílaba N veces |
| 2 | Reverse-repeat |
| 3-4 | Atenuar N en N+1 / todas excepto N |
| 5-6 | Repetir encogiendo desde fin/inicio |
| 7 | Dividir en N partes, repetir una |
| 8-9 | Repetir acortando desde fin/inicio |
| 10 | Extraer todas las sílabas |
| 11 | Reordenar aleatoriamente |

---

### 8.10 gate — Puerta de ruido
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Reemplaza bajo nivel con silencio |
| 2 | Edita bajo nivel (salida más corta) |

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| gatelevel | 0 a -96 dB | Umbral de gate |

---

## 9. SÍNTESIS

### 9.1 brownian — Textura browniana
- **Tipo:** WAV (usa source como waveform)
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| chans | int | | Canales de salida |
| dur | segundos | | Duración |
| att, dec | segundos | TV | Rise/decay de eventos (Modo 1) |
| plo, phi | MIDI | TV | Rango de pitch |
| step | semitonos | TV | Paso máximo de pitch |
| sstep | 0–1 | TV | Paso espacial máximo |
| tick | segundos | TV | Tiempo promedio entre eventos |
| -a arange | 0–96 dB | TV | Paso máximo de loudness |

---

### 9.2 chirikov — Mapas caóticos (Standard/Circle)
- **Tipo:** SYNTH
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| dur | segundos | | Duración |
| frq | Hz | TV | Frecuencia de conducción |
| damping | float | TV | Amortiguación |
| srate | int | | Sample rate |

---

### 9.3 crystal — Eventos desde vértices de cristal rotante en 3D
- **Tipo:** WAV (usa source)
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| vdat | archivo | Coordenadas X,Y,Z de vértices + envelope |
| rota, rotb | -10–10 rev/s | Velocidades de rotación |
| twidth | segundos | Tiempo máximo entre onsets de un grupo |
| tstep | segundos | Timestep entre muestreos del cristal |
| plo, phi | MIDI | Rango de pitch |

---

### 9.4 cascade — Echo-cascada de segmentos
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| clipsize | 0.005–60 s | TV | Duración de segmentos |
| echos | 1–64 | TV | Número de ecos |
| -r rand | 0–1 | TV | Randomiza timesteps |
| -N shredno | 2–16 | TV | Corta eco anterior en N partes |

---

### 9.5 cantor — Conjunto de Cantor (fractal)
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| holesize | % o segundos | Tamaño del agujero |
| holedig | >0–1 | Profundidad de cada corte |
| maxdur | segundos | Duración máxima |

---

### 9.6 fractal — Fractalización de sonido
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| layers | int | Número de capas fractales |
| -s splicelen | ms | Longitud de splices |

---

### 9.7 motor — Pulsos rápidos dentro de pulsos lentos
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| dur | segundos | | Duración |
| freq | 2–100 Hz | | Frecuencia del pulso interno |
| pulse | 0.1–10 Hz | | Frecuencia del pulso externo |
| fratio | 0–1 | | Proporción on/off interno |
| pratio | 0–1 | | Proporción on/off externo |
| sym | 0–1 | | Simetría (0.5=simétrico) |
| -j jitter | 0–3 st | | Pitch randomization |
| -t tremor | 0–1 | | Atenuación aleatoria |

---

### 9.8 synspline — Síntesis por splines aleatorios
- **Tipo:** SYNTH
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| frq | 0.001–10000 Hz | TV | Frecuencia fundamental |
| splinecnt | 0–64 | TV | Puntos aleatorios por half-wavecycle |
| interpval | 0–4096 | TV | Wavecycles de morphing |
| -d pdrift | 0–12 st | | Drift aleatorio de frecuencia |
| -v driftrate | 1–1000 ms | | Tiempo entre offsets de drift |

---

## 10. ESPACIAL Y MIXING

### 10.1 mchanpan — Panoramización multicanal (10 modos)
- **Tipo:** WAV / MONO → multicanal
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Pan por archivo de posiciones |
| 2 | Switch eventos entre canales |
| 3 | Spread stepwise entre sets de canales |
| 4 | Spread gradual desde centro |
| 5-6 | Antifonal entre 2 grupos |
| 7 | Pan entre configuraciones |
| 9 | Rotación continua |
| 10 | Switch aleatorio |

---

### 10.2 mchanrev — Ecos/reverb multicanal (stadium)
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| gain | float (dflt 0.645) | Ganancia de entrada |
| roll_off | float (dflt 1) | Pérdida de nivel |
| size | float | Multiplica spacing de ecos |
| count | int (dflt/max 1000) | Número de ecos |
| centre | 1–N | Posición central |
| spread | float | Ancho de distribución |

---

### 10.3 mchiter — Iteración multicanal fluida
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| outchans | int | | Canales de salida |
| -d delay | segundos | | Delay entre iteraciones |
| -r rand | 0–1 | | Randomización del delay |
| -p pshift | 0–12 st | | Pitch shift aleatorio |
| -a ampcut | 0–1 | | Reducción de amp aleatoria |
| -f fade | 0–1 | | Fade entre iteraciones |

---

### 10.4 mchshred — Shred multicanal
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| repeats | int | Pasadas de shredding |
| chunklen | segundos | Longitud promedio de chunk |
| scatter | 0–K | Randomización de cortes |

---

### 10.5 mchzig — Zigzag con pan aleatorio
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| start, end | segundos | Intervalo de zigzag |
| dur | segundos | Duración de salida |
| minzig | segundos | Tiempo mín entre zigzag |
| outchans | int | Canales de salida |

---

### 10.6 panorama — Distribuye monos en panorama espacial
- **Tipo:** WAV (mono inputs)
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| lspk_cnt | int | Número de altavoces |
| lspk_aw | 190–360° | Ancho angular del array |
| sounds_aw | ≤lspk_aw° | Ancho angular de distribución |
| -r rand | 0–1 | Randomización de posición |

---

### 10.7 modify space — Espacio stereo
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción | Parámetros |
|------|-------------|------------|
| 1 | Pan mono en stereo | `pan` (TV), `-p` prescale (dflt 0.7) |
| 2 | Mirror stereo | (sin params extra) |
| 4 | Narrow stereo | `narrowing` -1–1 (1=sin cambio, 0=mono) |

---

### 10.8 texmchan — Textura multicanal sobre campos armónicos
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| notedata | archivo | | Datos de pitch/armonía |
| outdur | segundos | | Duración mínima |
| packing | segundos | | Tiempo promedio entre eventos |
| scatter | 0–10 | | Randomización de onsets |
| mingain, maxgain | 1–127 | | Rango de nivel |
| mindur, maxdur | segundos | | Rango de duración |
| minpich, maxpich | MIDI | | Rango de pitch |
| outchans | int | | Canales de salida |
| -s spread | 1–outchans | | Spread espacial |

---

## 11. OTROS EFECTOS

### 11.1 flatten — Ecualizar nivel de elementos
- **Tipo:** WAV / MONO
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| elementsize | 0.001–100 s | Tamaño aprox de elementos |
| shoulder | 20ms–elementsize/2 | Risetime al nivel cambiado |

---

### 11.2 isolate — Cortar segmentos manteniendo timing
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1-2 | Corta por pares de tiempos |
| 3 | Corta por umbrales de nivel |
| 4-5 | Corta en tiempos de slice |

---

### 11.3 manysil — Insertar silencios en tiempos dados
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| silencedata | archivo | Pares tiempo-duración |
| splicelen | ms | Longitud de splice |

---

### 11.4 repeater — Repetir elementos con aceleración/bounce
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | TV | Descripción |
|-----------|-------|:--:|-------------|
| datafile | archivo | | Sets de (start, end, repeats, delay) |
| -r rand | 1–8 | TV | Randomización de delay |
| -p prand | 0–12 st | TV | Pitch aleatorio |
| accel | float | | Acortamiento de delay (Modo 3) |
| warp, fade | float | | Curva y decay (Modo 3) |

---

### 11.5 shifter — Ciclos de repetición con foco cambiante
- **Tipo:** WAV
- **Integrar:** `[ ]`

| Parámetro | Rango | Descripción |
|-----------|-------|-------------|
| cycles | archivo | Beats por ciclo |
| cycdur | segundos | Duración de un ciclo |
| dur | segundos | Duración de salida |
| ochans | int | Canales de salida |
| linger | int | Ciclos en foco fijo |
| transit | int | Ciclos de transición |
| boost | float | Nivel extra para el stream en foco |

---

### 11.6 frame — Manipulación de canales multicanal
- **Tipo:** WAV (multicanal)
- **Integrar:** `[ ]`

| Modo | Descripción |
|------|-------------|
| 1 | Rotar frame completo |
| 2 | Rotar pares/impares independientemente |
| 3 | Cambiar asignación de canales |
| 4 | Mirror |
| 6 | Swap par de canales |
| 7 | Envelopar canales independientemente |

---

## 12. RESUMEN RÁPIDO PARA ELEGIR

### Efectos más directamente integrables (WAV, pocos parámetros):

| # | Efecto | Tipo | Complejidad | Descripción corta |
|---|--------|------|:-----------:|-------------------|
| 1 | reverb | WAV | Media | Reverb clásico multicanal |
| 2 | rmverb | WAV | Media | Reverb con sala |
| 3 | sfecho | WAV | Baja | Echo simple |
| 4 | tapdelay | WAV | Media | Multi-tap delay stereo |
| 5 | filter variable | WAV | Baja | LP/HP/BP/Notch variable |
| 6 | filter sweeping | WAV | Media | Filtro con sweep |
| 7 | filter phasing | WAV | Baja | Phaser |
| 8 | tremolo | WAV | Baja | Tremolo |
| 9 | distort fractal | WAV/MONO | Baja | Distorsión fractal |
| 10 | distort reform | WAV/MONO | Baja | Cambia waveshape (8 tipos) |
| 11 | distort pitch | WAV/MONO | Baja | Transpone wavecycles aleatorio |
| 12 | bounce | WAV | Baja | Rebotes acelerados |
| 13 | clip | WAV | Baja | Recorte de señal |
| 14 | gate | WAV | Baja | Puerta de ruido |
| 15 | envel dovetail | WAV | Baja | Fade in/out |
| 16 | envel attack | WAV | Baja | Enfatizar ataque |
| 17 | envel warp | WAV | Media | 15 tipos de deformación |
| 18 | modify speed | WAV | Baja | Pitch/speed change |
| 19 | modify space | WAV | Baja | Pan stereo |
| 20 | hover | WAV | Media | Lectura granular zigzag |
| 21 | stutter | WAV | Media | Tartamudeo de sílabas |
| 22 | grain omit | WAV | Baja | Omitir granos |
| 23 | grain timewarp | WAV | Baja | Stretch sin estirar granos |
| 24 | grain reverse | WAV | Baja | Invertir orden de granos |
| 25 | wrappage | WAV | Alta | Granulación multicanal completa |
| 26 | scramble | WAV | Baja | Reordenar wavesets |
| 27 | constrict | WAV | Baja | Acortar silencios |
| 28 | quirk | WAV | Baja | Distorsión por potencia |
| 29 | fractal | WAV | Baja | Capas fractales de sonido |
| 30 | dvdwind | WAV | Baja | Contracción read-skip |

### Efectos spectrales (requieren pipeline specanal→efecto→pvoc):

| # | Efecto | Descripción corta |
|---|--------|-------------------|
| 31 | blur (10 modos) | Difuminado espectral |
| 32 | morph/newmorph | Morphing entre espectros |
| 33 | focus (7 modos) | Enfoque espectral |
| 34 | hilite (8 modos) | Resaltado espectral |
| 35 | specfnu (23 modos) | Manipulación de formantes |
| 36 | specfold | Plegar/invertir espectro |
| 37 | specsphinx | Cross-spectral |
| 38 | spectstr | Time-stretch espectral |
| 39 | spectwin | Interpolación espectral |
| 40 | stretch | Stretch de frecuencias |
| 41 | glisten | Partición aleatoria espectral |
