# 02 — Motor de Composicion: Arquitectura Interna

> Decisiones de diseno para v0.2: pipeline basado en tecnicas composicionales como presets abiertos,
> integracion de distribuciones Xenakis, cadenas de Markov, cribas, random walks y efectos multi-backend.

---

## 1. Pipeline v0.2 (nuevo)

### 1.1 Pipeline anterior (v0.1, referencia)

```
Sources (archivos audio)
    |
Arranger (orquesta todo)
    |
Strategy (scatter/structured/layer/canon)
    | usa
ControlledRandom (uniform, gaussian, markov_choice)
    | genera
Composition (lista de AudioEvents en tracks)
    |
Renderer -> Export (.wav/.mp3)
```

### 1.2 Pipeline v0.2

```
SOURCES (archivos audio)
    |
TECHNIQUE (preset composicional - define defaults para todo lo de abajo)
    |
STRATEGY (scatter / structured / layer / canon)
    |
STRUCTURE (derivada de la technique elegida)
    |
RNG: ControlledRandom (distribuciones originales + nuevas)
    |
EFFECTS (4 backends: Pedalboard, librosa, CDP, Granular)
    |
COMPOSITION (AudioEvents en tracks)
    |
Renderer -> Export
```

### 1.3 Sistema de override de 6 capas

Todo lo que establece una Technique es un DEFAULT que el usuario puede sobreescribir. El orden de prioridad (de menor a mayor) es:

```
technique -> strategy -> structure -> distributions -> ranges -> effects -> seed
```

Cada capa hereda los valores de la anterior salvo que el usuario los modifique explicitamente.

Cada AudioEvent mantiene: source, timeline_start, duration, amplitude, pan, fade_in, fade_out, effects_config, is_reversed.

---

## 2. Tecnicas composicionales (presets abiertos)

Las tecnicas son **presets abiertos, NO jaulas**. Definen valores por defecto para strategy, structure, distribuciones, rangos y efectos, pero el usuario puede modificar cualquier parametro.

| # | Tecnica | Concepto | Strategy default | Distribuciones clave | Efectos tipicos |
|---|---------|---------|-----------------|---------------------|----------------|
| 1 | **Xenakis (Stochastic)** | Procesos estocasticos formalizados | scatter / structured | Exponencial, Cauchy, Weibull, Poisson | Variados, controlados por distribuciones |
| 2 | **Feldman (Clusters)** | Agrupaciones suaves, dinamicas piano | layer | Gaussian para pitch/time, dinamicas soft | Reverb suave |
| 3 | **Ligeti (Micropolyphony)** | Densidad gaussiana, muchas capas superpuestas | layer | Gaussian (densidad), muchos tracks | Filtros sutiles |
| 4 | **Cage (Indeterminacy)** | Todo uniforme, maximo azar | scatter | Uniform para todo | Aleatorios, sin sesgo |
| 5 | **Scelsi (Deep Sound)** | Variacion minima de pitch, duraciones largas | layer | Gaussian muy estrecha (pitch), duraciones largas | Filtros lentos, reverb |
| 6 | **Reich (Phasing)** | Desfases microtemporales progresivos | canon | Canon con micro-offsets | Minimos |
| 7 | **Oliveros (Deep Listening)** | Eventos muy largos, espacialidad amplia | layer | Duraciones extremas | Reverb amplio, wide |
| 8 | **Lachenmann (Musique Concrete Instrumentale)** | Distorsion extrema, ruido | scatter / structured | Cauchy (saltos extremos) | Distorsion extrema, noise |
| 9 | **Saariaho (Spectralism)** | Transiciones suaves, efectos espectrales | layer / structured | Gaussian, walks suaves | Spectral, filtros smooth |
| 10 | **Nancarrow (Tempo Canons)** | Tempi independientes por track | canon | Independiente por track | Minimos |
| 11 | **Ferneyhough (New Complexity)** | Meta-tecnica: sub-tecnica diferente por track | Mixta | Sub-tecnica por track | Sub-tecnica por track |
| 12 | **Custom** | Preset en blanco, el usuario define todo | A elegir | A elegir | A elegir |

### Compatibilidad con v0.1

La tecnica **Cage (Indeterminacy)** con strategy scatter reproduce el comportamiento de v0.1 scatter (uniform en todo). Esto garantiza retrocompatibilidad.

---

## 3. Estrategias de composicion

### 3.1 Se mantienen las 4 estrategias de v0.1

| Estrategia | v0.1 | Mantener en v0.2 | Cambios |
|------------|------|-------------------|---------|
| scatter | Colocacion aleatoria pura | Si | Ahora recibe distribuciones de la technique (no solo uniform) |
| structured | Secciones con Markov (sparse/medium/dense/climax/silence) | Si | Matrices de transicion editables, presets por technique |
| layer | Capas texturales continuas | Si | Densidad de capas controlada por distribuciones |
| canon | Copias desfasadas de una secuencia base | Si | Soporta micro-offsets (Reich) y tempi independientes (Nancarrow) |

### 3.2 Nuevas estrategias

No se anaden nuevas estrategias. Las 4 existentes cubren todos los casos necesarios. La variedad composicional viene de las **techniques** (presets), no de multiplicar strategies.

---

## 4. Distribuciones de probabilidad (Xenakis)

### 4.1 Distribuciones disponibles en ControlledRandom

| Distribucion | Incluir | Para que parametros | Caracter |
|-------------|---------|--------------------|----|
| Uniform | Ya existe (v0.1) | Todos | Azar puro, sin sesgo |
| Gaussian | Ya existe (v0.1) | Todos | Agrupacion alrededor de centro |
| Markov choice | Ya existe (v0.1) | Seleccion discreta | Transiciones dependientes del estado |
| **Exponencial** | Si (nueva) | timeline_start, duration, density | Rafagas agrupadas, silencios largos |
| **Cauchy** | Si (nueva) | pitch, amplitude, pan | Colas extremas, saltos impredecibles |
| **Weibull** | Si (nueva) | duration, density | Forma ajustable con parametro k |
| **Poisson** | Si (nueva) | conteo de eventos por seccion | Distribucion discreta de frecuencia |

### 4.2 Sieves (cribas de Xenakis) para cuantizacion

Ademas de las distribuciones continuas, se incluyen **sieves** como mecanismo de cuantizacion post-distribucion (ver seccion 6).

### 4.3 Random walks para evolucion de parametros

Los random walks complementan las distribuciones generando evolucion temporal coherente (ver seccion 7).

### 4.4 Donde se insertan en el pipeline

**Decision: Opcion C** — Las distribuciones se pueden usar DURANTE la generacion de la strategy (reemplazando las llamadas internas a rng.uniform/gaussian) Y como post-procesado despues de que la strategy genera los eventos.

Esto da maxima flexibilidad: la technique define que distribuciones usa la strategy internamente, y ademas puede aplicar transformaciones post-generacion.

---

## 5. Cadenas de Markov

### 5.1 Que controlan las cadenas de Markov

| Parametro | Markov | Estados posibles | Ejemplo |
|-----------|--------|-----------------|---------|
| Tipo de seccion (densidad) | Si | sparse, medium, dense, climax, silence | Ya existe en structured, se mantiene |
| Seleccion de source | Si | Nombres de archivos cargados | Despues de piano -> 70% cello |
| Dinamica | Si | pp, p, mp, mf, f, ff | Crescendo probabilistico |
| Efecto aplicado | Si | reverb, delay, granular, filter... | Despues de reverb -> delay |

### 5.2 Matriz de transicion

- **El usuario puede editar la matriz en la GUI:** Si. Se ofrece un editor de matriz visual.
- **Presets predefinidos:** Si. Cada technique define matrices por defecto coherentes con su estetica (ej. Feldman: transiciones suaves entre dinamicas bajas; Lachenmann: saltos abruptos).
- **Orden:** Orden 1 (depende del ultimo estado).

### 5.3 Multiples cadenas en paralelo

**Si.** Se pueden tener varias cadenas de Markov funcionando simultaneamente (una para source, otra para dinamica, otra para efectos, etc.). Cada cadena opera de forma independiente con su propia matriz de transicion.

---

## 6. Cribas (Sieves)

### 6.1 Parametros que pueden filtrarse con cribas

| Parametro | Criba | Unidad de discretizacion | Ejemplo |
|-----------|-------|-------------------------|---------|
| timeline_start (ritmo) | Si | centesimas de segundo | Sieve(25,0) -> cada 0.25s |
| duration | Si | decimas de segundo | Solo duraciones 0.5, 1.0, 1.5... |
| amplitude | Si | niveles discretos | Solo pp y ff |
| pan | Si | posiciones discretas | 4 puntos fijos en estereo |

### 6.2 Como define el usuario la criba

- **Pares (modulo, residuo) manualmente:** Si. El usuario introduce pares (modulo, residuo) en la GUI.
- **Presets:** Si. Cada technique puede definir cribas por defecto (ej. Xenakis: cribas complejas; Cage: sin cribas).
- **Combinaciones logicas:** Si. Se soportan union, interseccion y complemento de cribas, siguiendo la formalizacion original de Xenakis.

### 6.3 Que pasa cuando un valor no pasa la criba

**Se cuantiza al valor mas cercano que SI pasa la criba.** No se descarta ni se regenera. Esto garantiza que la cantidad de eventos generados por la strategy no cambia, solo se ajustan sus valores a la rejilla definida por la criba.

---

## 7. Random Walks (paseos aleatorios)

### 7.1 Parametros que controla el random walk

| Parametro | Walk | step_size tipico | Frontera |
|-----------|------|-----------------|----------|
| pan | Si | Configurable | reflectante / absorbente / wrap |
| amplitude | Si | Configurable | reflectante / absorbente / wrap |
| density (gap entre eventos) | Si | Configurable | reflectante / absorbente / wrap |
| parametros de efecto (wet/dry, etc.) | Si | Configurable | reflectante / absorbente / wrap |
| source_start (offset en el archivo) | Si | Configurable | reflectante / absorbente / wrap |

### 7.2 Parametros del walk configurables por el usuario

- **step_size (tamano del paso):** Si. Configurable por el usuario.
- **Tipo de frontera:** Si. El usuario elige entre reflectante (rebota), absorbente (se queda en el limite) o wrap (aparece en el otro extremo).
- **Drift (tendencia direccional):** Si. Permite sesgar el walk en una direccion (ej. crescendo gradual).
- **Valor inicial:** Si. Configurable o aleatorio segun seed.

---

## 8. Efectos: aleatorizacion de parametros

### 8.1 Backends de efectos

v0.2 integra 4 backends de procesamiento de audio:

| Backend | Tecnologia | Uso principal |
|---------|-----------|--------------|
| **Pedalboard** | Spotify Pedalboard (Python) | Efectos estandar en tiempo real: reverb, delay, chorus, compressor |
| **librosa STFT** | librosa (Python) | Procesamiento espectral: time-stretch, pitch-shift |
| **CDP** | Composers Desktop Project (subprocess) | Transformaciones avanzadas: spectral, granular CDP |
| **Granular** | Motor granular propio (Python) | Sintesis granular personalizada |

### 8.2 Grupos de efectos

8 grupos organizan los efectos disponibles:

1. **Dynamics** — compressor, limiter, gate
2. **Reverb & Delay** — reverb, delay, echo
3. **Filter** — lowpass, highpass, bandpass, EQ
4. **Distortion** — distortion, bitcrush, noise
5. **Modulation** — chorus, flanger, phaser, tremolo
6. **Pitch & Time** — pitch-shift, time-stretch
7. **Granular** — granular synthesis, fragmentacion
8. **Spectral** — spectral freeze, blur, morph

### 8.3 Migracion de efectos existentes (18 efectos v0.1)

| Accion | Cantidad | Descripcion |
|--------|----------|-------------|
| **Mantener** tal cual | 7 | Funcionan bien con Pedalboard/librosa |
| **Mejorar** con CDP | 7 | Se mantiene la version actual y se anade variante CDP |
| **Reemplazar** con CDP | 4 | La version CDP es objetivamente superior |

### 8.4 Aleatorizacion de parametros de efectos

**Decision: Opcion D** — Depende de la technique.

El sistema funciona asi:
1. **Markov** elige QUE efecto aplicar (cadena de transicion entre efectos)
2. **Distribucion** (de la technique) elige los valores iniciales de los parametros del efecto
3. **Random walk** evoluciona los parametros de evento en evento (ej. wet/dry de reverb cambia gradualmente)

Esto reemplaza el comportamiento de v0.1 donde los parametros de efectos se enviaban vacios (`{}`) y siempre usaban defaults. Ahora cada technique define un perfil coherente de efectos.

---

## 9. Orden de aplicacion (pipeline interno por evento)

Al generar cada evento, las tecnicas Xenakis se aplican en este orden:

```
1. Markov decide contexto/estado (seccion, source, dinamica, efecto)
        |
2. Distribucion genera valor crudo (segun technique + override del usuario)
        |
3. Criba filtra valores invalidos (cuantiza al mas cercano valido)
        |
4. Random Walk suaviza evolucion temporal (aplica paso desde valor anterior)
```

Este orden se mantiene tal como fue propuesto en el documento de referencia. La logica es:
- Markov establece el **contexto macro** (en que seccion estamos, que fuentes usar)
- La distribucion genera los **valores micro** dentro de ese contexto
- La criba **cuantiza** esos valores a la rejilla deseada
- El walk **suaviza** la transicion entre eventos consecutivos

---

## 10. Reproducibilidad

- **Misma seed + misma config = mismo resultado siempre:** Si. Esto es un requisito absoluto.
- **El sistema Xenakis respeta la seed maestra:** Si. Todas las distribuciones, cadenas de Markov, cribas y random walks se inicializan desde la seed maestra. Cambiar la seed produce un resultado diferente pero determinista; mantener la seed produce un resultado identico.

---

## 11. Resumen de decisiones

| Aspecto | Decision |
|---------|----------|
| Techniques | 11 presets abiertos + Custom |
| Strategies | 4 (scatter, structured, layer, canon) — sin cambios |
| Override | 6 capas: technique -> strategy -> structure -> distributions -> ranges -> effects -> seed |
| Distribuciones nuevas | Exponencial, Cauchy, Weibull, Poisson |
| Distribuciones en pipeline | Opcion C: durante generacion Y post-procesado |
| Markov | Orden 1, multiples cadenas paralelas, matrices editables |
| Cribas | 4 parametros, pares (mod, res), combinaciones logicas, cuantizacion |
| Random walks | 5 parametros, step/frontera/drift/inicial configurables |
| Efectos backends | 4: Pedalboard, librosa, CDP, Granular |
| Efectos parametros | Opcion D: Markov elige efecto, distribucion elige params, walk evoluciona |
| Efectos migracion | 7 mantener, 7 mejorar con CDP, 4 reemplazar con CDP |
| Reproducibilidad | Garantizada con seed maestra |
