# 05 — Tecnicas Compositivas: Presets Abiertos para v0.2

> "No quiero encasillar las composiciones. Para eso es un Aleatoric compositor."
> Las tecnicas son **puntos de partida**, no jaulas. Todo es sobreescribible.

---

## 1. Filosofia: Presets, no celdas

Cada tecnica compositiva funciona como un **PRESET ABIERTO**: un conjunto de defaults inteligentes que el usuario puede modificar en cualquier nivel. La idea es que al seleccionar "Xenakis" o "Feldman", el motor configure automaticamente distribuciones, efectos, densidades y duraciones coherentes con esa estetica — pero el usuario tiene **control total** para desviarse.

### 1.1 Sistema de override en 6 capas

```
Capa 1: TECNICA         → Preset base (Xenakis, Feldman, etc.)
Capa 2: ESTRATEGIA      → scatter / layer / canon / structured
Capa 3: ESTRUCTURA       → duracion, tracks, curva de densidad
Capa 4: DISTRIBUCIONES  → timing, amplitude, duration, pan
Capa 5: RANGOS          → min/max de cada parametro
Capa 6: EFECTOS + SEED  → cadena de efectos, semilla RNG
```

Cada capa inferior sobreescribe a la superior. Si el usuario cambia la distribucion de timing, se mantiene todo lo demas del preset.

### 1.2 Pipeline de composicion

```
SOURCES (archivos audio)
    ↓
TECNICA (preset de defaults)
    ↓
ESTRATEGIA (scatter/structured/layer/canon)
    ↓
ESTRUCTURA (duracion total, n_tracks, densidad)
    ↓
RNG (distribuciones → eventos)
    ↓
EFECTOS (cadena CDP por evento/track)
    ↓
COMPOSICION (AudioEvents en timeline)
```

---

## 2. Catalogo de tecnicas

---

### 2.1 Xenakis — Estocastica

> Musica estocastica: nubes de probabilidad, masas sonoras controladas por distribuciones matematicas.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `scatter` |
| **Duracion** | 120–300 s |
| **Tracks** | 4–8 |
| **Curva densidad** | `arc` (crece → climax → decrece) |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Timing | Exponencial | Rafagas agrupadas con silencios |
| Amplitud | Cauchy | Colas extremas, picos impredecibles |
| Duracion eventos | Weibull (k variable) | Forma ajustable segun seccion |
| Conteo eventos | Poisson | Discreto, natural para conteos |

**Efectos afines:** `distortion`, `scramble`, `granular`, `wrappage`, `filter_bank`, `sp_smear`, `fractal`

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | Si | Transiciones de densidad entre secciones |
| Cribas (sieves) | Si | Cuantizacion de pitch y tiempo |
| Random walks | Si | Evolucion de pan y amplitud |

---

### 2.2 Feldman — Clusters suaves

> Quietud, estatismo, clusters flotantes. Sonido que apenas se mueve.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `layer` |
| **Duracion** | 180–600 s |
| **Tracks** | 3–6 |
| **Curva densidad** | `constant` (baja) |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Timing | Gaussian (estrecha) | Eventos espaciados regularmente |
| Amplitud | Gaussian (estrecha) | Rango muy limitado |
| Pan | Uniform | Distribucion espacial pareja |

**Rango de amplitud:** 0.05–0.3 (muy suave, siempre pianissimo)

**Efectos afines:** `reverb`, `gain` (bajo), `envel_dovetail`, `envel_warp`, `modify_space`, `flatten`

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | No | — |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.3 Ligeti — Micropolifonia

> Nubes densas de micro-eventos que crean textura. Muchas voces independientes fusionandose.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `layer` |
| **Duracion** | 60–180 s |
| **Tracks** | 8–16 |
| **Curva densidad** | `crescendo` (baja → muy alta) |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Timing | Gaussian (muy estrecha) | Clusters temporales apretados |
| Pitch spread | Uniform | Expansion cromatica gradual |

**Densidad de eventos:** Muy alta. Eventos cortos (50–500 ms).

**Efectos afines:** `sp_smear`, `chorus`, `phaser`, `granular`, `hover`, `wrappage`

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | No | — |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.4 Cage — Indeterminacion

> Azar puro, sin preferencias. Compatible hacia atras con el `scatter` de v0.1.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `scatter` |
| **Duracion** | 60–300 s |
| **Tracks** | 2–8 |
| **Curva densidad** | `constant` |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Timing | Uniform | Sin preferencia |
| Amplitud | Uniform | Sin preferencia |
| Duracion eventos | Uniform | Sin preferencia |
| Pan | Uniform | Sin preferencia |

**Efectos afines:** TODOS los grupos (cualquier efecto es igualmente probable)

**Nota:** Esta es la **tecnica nula** — reproduce el comportamiento de v0.1. Al seleccionar Cage, el motor no impone ninguna tendencia estetica. Todo parametro tiene probabilidad uniforme.

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | No | — |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.5 Scelsi — Sonido profundo

> Explorar un unico sonido en profundidad. Micro-variaciones sobre material minimo.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `layer` |
| **Duracion** | 300–900 s |
| **Tracks** | 2–4 |
| **Curva densidad** | `constant` (muy baja) |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Pitch | Gaussian (muy estrecha) | Orbitar un centro unico |
| Duracion eventos | Exponencial | Eventos largos, sostenidos |

**Efectos afines:** `sp_freeze`, `sp_shift`, `sp_smear`, `time_stretch`, `granular`

**Estetica:** Texturas largas, sostenidas. Variacion minima. El interes esta en la transformacion timbrica interna del sonido.

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | No | — |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.6 Reich — Phasing

> Repeticion con desfase gradual. Patrones que se desalinean lentamente.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `canon` |
| **Duracion** | 120–480 s |
| **Tracks** | 3–6 |
| **Curva densidad** | `constant` |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Micro-offsets | Uniform (estrecha) | Desfases minimos entre tracks |

**Efectos afines:** `delay`, `reverb`

**Mecanismo:** Canon con diferencias de tempo minimas entre tracks. Track 1 a 1.000x, Track 2 a 1.002x, Track 3 a 0.998x, etc. El desfase acumulado genera el efecto de phasing.

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | No | — |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.7 Oliveros — Deep Listening

> Sonido sostenido, meditativo. Espacio acustico amplio y envolvente.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `layer` |
| **Duracion** | 300–1200 s |
| **Tracks** | 2–4 |
| **Curva densidad** | `constant` (minima) |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Timing | Gaussian (centrada, estrecha) | Eventos espaciados regularmente |
| Amplitud | Gaussian (centrada, estrecha) | Dinamica muy estable |

**Efectos afines:** `reverb` (largo), `delay`, `envel_warp`, `modify_space`, `envel_dovetail`

**Estetica:** Eventos muy largos. Reverb dominante. La composicion es mas espacio que contenido.

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | No | — |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.8 Lachenmann — Musique Concrete Instrumentale

> Tecnicas extendidas, ruido como material. Procesamiento agresivo.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `structured` (Markov) |
| **Duracion** | 60–240 s |
| **Tracks** | 4–8 |
| **Curva densidad** | `wave` (ondulante) |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Timing | Cauchy | Saltos extremos, impredecible |
| Amplitud | Exponencial | Rafagas con picos subitos |

**Efectos afines:** `distortion`, `bitcrush`, `clip`, `quirk`, `scramble`, `granular`, `filter`

**Estetica:** Contrastes agudos. Procesamiento pesado que transforma el material hasta hacerlo irreconocible. Silencios subitos.

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | Si | Transiciones entre estados (ruido/tono/silencio) |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.9 Saariaho — Espectralismo

> Transformaciones espectrales suaves. Evolucion timbrica continua.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `structured` (Markov) |
| **Duracion** | 120–360 s |
| **Tracks** | 4–8 |
| **Curva densidad** | `arc` |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Timing | Gaussian | Transiciones suaves |
| Duracion eventos | Weibull | Forma ajustable, tendencia a largos |

**Efectos afines:** `sp_freeze`, `sp_smear`, `sp_shift`, `sp_gate`, `granular`, `time_stretch`

**Estetica:** Foco en efectos espectrales (CDP spectral domain). La composicion navega entre estados timbrales.

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | Si | Transiciones entre estados espectrales |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.10 Nancarrow — Tempo Canons

> Tempi independientes por track. Poliritmia extrema.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `canon` |
| **Duracion** | 60–240 s |
| **Tracks** | 3–8 |
| **Curva densidad** | `constant` |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Timing por track | Uniform (con multiplicadores diferentes) | Cada track tiene su propio tempo |

**Efectos afines:** `pitch_shift`, `time_stretch`

**Mecanismo:** Cada track recibe un ratio de tempo diferente. Ej: Track 1 = 1.0x, Track 2 = 1.33x, Track 3 = 0.75x, Track 4 = 1.5x. Los patrones convergen y divergen ciclicamente.

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | No | — |
| Cribas (sieves) | No | — |
| Random walks | No | — |

---

### 2.11 Ferneyhough — Nueva Complejidad

> Complejidad maxima. Meta-tecnica que combina sub-tecnicas por track.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `structured` (Markov) |
| **Duracion** | 60–180 s |
| **Tracks** | 6–12 |
| **Curva densidad** | `wave` (ondulante) |

**Distribuciones:**

| Parametro | Distribucion | Justificacion |
|-----------|-------------|---------------|
| Mixta | Cada track puede usar una sub-tecnica DIFERENTE | Maximiza la independencia entre voces |

**Efectos afines:** TODOS los grupos

**META-TECNICA:** Ferneyhough es unica porque cada track puede tener asignada su propia sub-tecnica. Track 1 podria usar distribuciones Xenakis, Track 2 distribuciones Feldman, Track 3 distribuciones Ligeti, etc. El resultado es una complejidad polifonica donde cada voz tiene su propia logica interna.

**Caracteristicas especiales:**

| Herramienta | Activa | Uso |
|-------------|--------|-----|
| Cadenas de Markov | Si | Control de forma global |
| Cribas (sieves) | Opcional | Dependiendo de sub-tecnica |
| Random walks | Opcional | Dependiendo de sub-tecnica |

---

### 2.12 Custom — Preset vacio

> Pizarra en blanco. El usuario define todo desde cero.

| Parametro | Default |
|-----------|---------|
| **Estrategia** | `scatter` (neutral) |
| **Duracion** | 120 s |
| **Tracks** | 4 |
| **Curva densidad** | `constant` |

**Distribuciones:** Todas `uniform` (neutral).

**Efectos:** Ninguno pre-seleccionado.

**Uso:** Para usuarios que quieren construir su propia estetica sin partir de ningun referente. Todos los parametros en valores neutros/default.

---

## 3. Implementacion

### 3.1 Clases Python

12 clases, todas heredando de `CompositionTechnique`:

```python
class CompositionTechnique(ABC):
    """Clase base para todas las tecnicas compositivas."""

    @abstractmethod
    def get_defaults(self) -> dict:
        """Retorna diccionario con todos los defaults del preset."""
        ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def strategy(self) -> str: ...


class XenakisTechnique(CompositionTechnique): ...
class FeldmanTechnique(CompositionTechnique): ...
class LigetiTechnique(CompositionTechnique): ...
class CageTechnique(CompositionTechnique): ...
class ScelsiTechnique(CompositionTechnique): ...
class ReichTechnique(CompositionTechnique): ...
class OliverosTechnique(CompositionTechnique): ...
class LachenmannTechnique(CompositionTechnique): ...
class SaariahoTechnique(CompositionTechnique): ...
class NancarrowTechnique(CompositionTechnique): ...
class FerneyhoughTechnique(CompositionTechnique): ...
class CustomTechnique(CompositionTechnique): ...
```

### 3.2 Merge de configuracion

El `Arranger` fusiona capas en este orden:

```python
# Prioridad: user_overrides > technique defaults
final_config = {
    **technique.get_defaults(),   # Capa 1: preset base
    **user_overrides,             # Capas 2-6: lo que el usuario cambie
}
```

Todo valor del preset puede ser sobreescrito. El usuario nunca esta atrapado.

---

## 4. Tablas de mapeo

### 4.1 Tecnica x Distribuciones por defecto

| Tecnica | Timing | Amplitud | Duracion | Pan |
|---------|--------|----------|----------|-----|
| Xenakis | Exponencial | Cauchy | Weibull | Uniform |
| Feldman | Gaussian (e) | Gaussian (e) | Gaussian | Uniform |
| Ligeti | Gaussian (me) | Uniform | Uniform (corta) | Uniform |
| Cage | Uniform | Uniform | Uniform | Uniform |
| Scelsi | Gaussian (e) | Gaussian (e) | Exponencial | Gaussian |
| Reich | Uniform (e) | Uniform (e) | Uniform (e) | Uniform |
| Oliveros | Gaussian (e) | Gaussian (e) | Exponencial | Gaussian |
| Lachenmann | Cauchy | Exponencial | Cauchy | Uniform |
| Saariaho | Gaussian | Gaussian | Weibull | Gaussian |
| Nancarrow | Uniform (x track) | Uniform | Uniform | Uniform |
| Ferneyhough | Mixta | Mixta | Mixta | Mixta |
| Custom | Uniform | Uniform | Uniform | Uniform |

> **(e)** = estrecha, **(me)** = muy estrecha

### 4.2 Tecnica x Afinidad de efectos

| Tecnica | Efectos principales | Efectos secundarios |
|---------|--------------------|--------------------|
| Xenakis | distortion, scramble, granular | wrappage, filter_bank, sp_smear, fractal |
| Feldman | reverb, gain (bajo) | envel_dovetail, envel_warp, modify_space, flatten |
| Ligeti | sp_smear, chorus, phaser | granular, hover, wrappage |
| Cage | TODOS | TODOS |
| Scelsi | sp_freeze, sp_shift, sp_smear | time_stretch, granular |
| Reich | delay, reverb | — |
| Oliveros | reverb (largo), delay | envel_warp, modify_space, envel_dovetail |
| Lachenmann | distortion, bitcrush, clip | quirk, scramble, granular, filter |
| Saariaho | sp_freeze, sp_smear, sp_shift | sp_gate, granular, time_stretch |
| Nancarrow | pitch_shift, time_stretch | — |
| Ferneyhough | TODOS | TODOS |
| Custom | — | — |

---

## 5. Resumen visual

```
┌─────────────────────────────────────────────────────┐
│                TECNICA (preset)                      │
│  ┌───────────────────────────────────────────────┐  │
│  │  strategy + structure + distributions +       │  │
│  │  ranges + effects + markov + sieves + walks   │  │
│  └───────────────────────────────────────────────┘  │
│                      ↓                               │
│           USER OVERRIDES (cualquier capa)            │
│                      ↓                               │
│              CONFIGURACION FINAL                     │
│                      ↓                               │
│       Arranger → Strategy → RNG → Composition       │
└─────────────────────────────────────────────────────┘
```

> Cada tecnica es un punto de partida. El destino lo decide el compositor.
