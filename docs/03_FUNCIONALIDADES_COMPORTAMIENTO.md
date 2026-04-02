# 03 — Funcionalidades y Comportamiento

> Qu hace cada control, qu feedback recibe el usuario, flujos de interaccion.
> Conecta el diseno visual (doc 01) con el motor interno (doc 02).
> **Version:** v0.2 — Aleatoric Composer con 11 tecnicas compositivas como OPEN PRESETS.

---

## 1. Flujo principal del usuario

### 1.1 Flujo v0.1 (referencia)

```
1. Cargar audio -> panel Sources (drag & drop o boton)
2. Ajustar pesos de cada source
3. Elegir estrategia + configurar parametros -> tab Composition
4. (Opcional) Ajustar defaults de efectos -> tab Effects Palette
5. Pulsar Compose -> se genera la composicion (aparece en el timeline)
6. Pulsar Re-roll -> nueva composicion con seed diferente
7. Pulsar Render -> se renderiza a audio (barra de progreso)
8. Pulsar Export WAV/MP3 -> se guarda el archivo
```

### 1.2 Flujo v0.2

El flujo cambia significativamente. Se anade la seleccion de **tecnica compositiva** como paso central, y se introducen overrides opcionales en cascada. El pipeline interno es: **TECHNIQUE -> STRATEGY -> STRUCTURE -> RNG -> EFFECTS**.

```
1.  Cargar audio -> panel Sources (drag & drop o boton)
2.  Ajustar pesos de cada source
3.  Seleccionar TECNICA COMPOSITIVA (preset) -> configura defaults para todo
4.  (Opcional) Override de Strategy (scatter/structured/layer/canon)
5.  (Opcional) Override de Structure parameters
6.  (Opcional) Ajustar distribuciones RNG por parametro
7.  (Opcional) Configurar efectos
8.  Pulsar Compose -> genera composicion con pipeline completo
9.  Re-roll -> nueva seed, misma config
10. Render -> audio
11. Export WAV/MP3/FLAC + JSON
```

**Cambios clave respecto a v0.1:**
- Se anade el paso 3 (tecnica compositiva) como punto de entrada principal.
- Los pasos 4-7 son overrides opcionales — el preset de la tecnica provee defaults razonables para todo.
- Se anade exportacion JSON (composicion y configuracion).
- Las tecnicas son **OPEN PRESETS**, no jaulas: el usuario tiene libertad total para sobreescribir cualquier parametro.

---

## 2. Boton Compose

### 2.1 Que pasa al pulsar Compose?

> **v0.1:** Lee sources + pesos + constraints + strategy -> Arranger.compose() -> muestra en timeline.

**v0.2:** El boton Compose ejecuta el pipeline de 6 capas de override:

1. Lee la **tecnica compositiva** seleccionada (preset base).
2. Aplica cualquier **override de Strategy** que el usuario haya configurado.
3. Aplica cualquier **override de Structure** (parametros de estructura).
4. Aplica cualquier **override de distribuciones RNG** por parametro.
5. Aplica configuracion de **efectos** (habilitados/deshabilitados, rangos).
6. Ejecuta `Arranger.compose()` con la configuracion resultante.
7. Muestra la composicion en el **timeline**.

**Se leen los parametros de Xenakis (distribuciones, Markov, cribas, walks)?** Si. Todos los parametros de las tecnicas compositivas se leen como parte del preset o de los overrides del usuario. Cada tecnica define sus propios defaults para distribuciones, cadenas de Markov, cribas y random walks segun corresponda.

**Feedback adicional:** No se anade feedback extra en v0.2 (ni estadisticas ni graficos de distribucion post-composicion). El timeline es el feedback principal. Se evaluan estadisticas y visualizaciones post-compose para v0.3.

### 2.2 Tiempo de composicion

La composicion debe ser **rapida**: menos de 2 segundos para composiciones normales (hasta ~500 eventos). No se muestra barra de progreso para Compose — el boton se desactiva momentaneamente y el timeline se actualiza al completar. Si una composicion excepcionalmente larga supera los 5 segundos, se muestra un spinner simple sobre el timeline.

---

## 3. Boton Re-roll

> **v0.1:** Genera nueva seed, recompone con mismos parametros.

**v0.2:** El comportamiento base se mantiene identico. Re-roll genera una nueva seed aleatoria y ejecuta el mismo pipeline de composicion con todos los parametros actuales (tecnica + overrides) intactos.

**Re-roll parcial (solo una tecnica o capa)?** No. En v0.2 no se soporta re-roll parcial. La complejidad de re-generar solo una capa del pipeline (e.g., solo los estados Markov manteniendo el resto) es demasiado alta para esta version. Re-roll siempre recompone todo. Se reevalua para v0.3.

---

## 4. Controles de composicion

### 4.1 Strategy selector

Al cambiar de estrategia (scatter / structured / layer / canon):

- **No se recompone automaticamente.** El cambio solo toma efecto en la proxima pulsacion de Compose. Esto es intencional: permite al usuario ajustar multiples parametros antes de recomponer.
- **Se muestran/ocultan controles segun la estrategia.** Ejemplo: la matriz de Markov solo se muestra cuando la estrategia es `structured`. Los controles de canon (intervalo, voces) solo aparecen con `canon`. Los controles irrelevantes se ocultan con animacion de fade-out para evitar saltos bruscos en el layout.

### 4.2 Seed

- **Se muestra la seed actual:** Si, como campo de texto de solo lectura debajo del boton Re-roll, en fuente monoespaciada (DM Mono).
- **Boton Random para nueva seed:** Si, icono de dado junto al campo de seed. Equivale funcionalmente a Re-roll pero sin ejecutar Compose.
- **Copiar/pegar seed:** Si. Click en la seed la copia al portapapeles (con feedback visual: el texto parpadea brevemente en Amber #FBAD17). Se puede pegar una seed manualmente para reproducir una composicion exacta.

### 4.3 Density curve

Se mantienen las **5 curvas existentes**: constant, crescendo, decrescendo, arc, wave.

Se anade una **sexta opcion: "custom"** (curva dibujable). Al seleccionar "custom", aparece un area de dibujo donde el usuario puede trazar una curva de densidad a mano libre con el raton. La curva se normaliza automaticamente al rango [0, 1]. Se puede resetear con un boton "Clear".

---

## 5. Controles de tecnicas compositivas

### 5.1 Activacion y modelo de presets

En v0.2 **no hay switch ON/OFF global** para las tecnicas. El sistema funciona con **presets abiertos**:

- El usuario selecciona una tecnica compositiva en el tab **Technique** (12 opciones: 11 tecnicas + "Custom/Blank").
- La tecnica seleccionada carga defaults para: strategy, structure, distribuciones RNG, efectos preferidos, y parametros especificos.
- El usuario puede sobreescribir **cualquier parametro** libremente. La tecnica es un punto de partida, no una restriccion.
- Si el usuario selecciona "Custom/Blank", comienza sin defaults — equivalente al comportamiento de v0.1.
- Si todas las tecnicas estan en sus defaults (ninguna seleccionada, o "Custom/Blank"), la app se comporta exactamente como v0.1.

### 5.2 Distribuciones

Cuando el usuario elige una distribucion (e.g., Cauchy para pan, Exponencial para duracion):

- **Feedback visual:** Se muestra un **preview de la curva** de la distribucion seleccionada, integrado en el combo-box. Es una miniatura estatica (64x32px) que se actualiza al cambiar parametros. No es un histograma interactivo — es una representacion visual rapida de la forma de la distribucion.
- **Parametros ajustables:** Si. Cada distribucion expone sus parametros clave (lambda para Exponencial, gamma para Cauchy, k/theta para Weibull, etc.) como sliders con valores numericos editables.
- **Tooltips:** Si. Cada distribucion tiene un tooltip que explica en una frase que tipo de valores tiende a generar (e.g., "Cauchy: valores concentrados en el centro con colas pesadas — genera outliers frecuentes").

### 5.3 Markov

Cuando el usuario configura una cadena de Markov:

- **Matriz como tabla editable:** Si. Se muestra una tabla NxN donde N es el numero de estados. Las celdas son editables y las filas se normalizan automaticamente a suma 1.0 al perder el foco.
- **Grafo visual de estados:** No en v0.2. La complejidad de renderizar y mantener sincronizado un grafo interactivo es demasiado alta. Se planea para v0.3.
- **Importar/exportar matrices:** Si, como JSON. Boton "Export Matrix" y "Import Matrix" junto a la tabla.
- **Preview de cadena:** No en v0.2. No hay boton de preview que muestre estados generados antes de componer.

### 5.4 Cribas (Sieves)

Cuando el usuario define una criba:

- **Visualizacion step-sequencer:** Si. Se muestra una grilla tipo step-sequencer donde los pasos activos (valores que pasan la criba) se iluminan en Amber (#FBAD17) y los inactivos quedan en Slate (#303C42). El usuario introduce modulo y residuo como inputs numericos, y la grilla se actualiza en tiempo real.
- **Combinacion de cribas:** Si, con botones de union (U), interseccion (^) y complemento (~). Se pueden apilar multiples cribas.
- **Preview auditiva del patron ritmico:** No en v0.2. Solo visualizacion.

### 5.5 Random Walks

Cuando el usuario configura un random walk:

- **Preview de trayectoria:** Si. Se muestra una miniatura (128x64px) con una trayectoria de ejemplo generada con la seed actual. Se actualiza en tiempo real al cambiar parametros.
- **Slider de step_size:** Si. Slider horizontal con valor numerico editable, rango dependiente del parametro objetivo.
- **Diferencia visual entre fronteras:** Si. Un combo-box selecciona el tipo de frontera (reflectante / absorbente / wrap) y la preview de trayectoria refleja el comportamiento: la trayectoria rebota, se detiene, o envuelve al llegar al limite, respectivamente.

---

## 6. Efectos

### 6.1 Seleccion de efectos

> **v0.1:** Todos los efectos estan siempre disponibles. effects_probability y max_effects_per_event controlan cuantos se aplican.

**v0.2:** El usuario puede **activar/desactivar efectos individuales** en el tab Effects Palette. Se organizan en 8 familias de efectos, cada una con toggle individual. Los efectos desactivados nunca se aplican, independientemente de effects_probability.

- **Activar/desactivar efectos individuales:** Si. Toggle switch por cada efecto.
- **Excluir ciertos efectos:** Si, equivale a desactivar su toggle. Ademas, cada tecnica compositiva (preset) pre-configura que efectos estan habilitados por defecto — el usuario puede sobreescribir.

### 6.2 Parametros de efectos

Los parametros de efectos son **aleatorios por defecto**, controlados por la tecnica compositiva seleccionada. El usuario tiene dos niveles de control:

- **Slider de "randomizacion" por efecto:** Un slider (0%-100%) controla cuanto varian los parametros del efecto respecto a su valor base. Al 0%, los parametros son fijos en su valor default. Al 100%, varian en todo su rango permitido.
- **Min/max por parametro:** No expuestos directamente en v0.2. El rango lo define la tecnica. Para control fino, el usuario puede cambiar a la tecnica "Custom/Blank" y ajustar manualmente.

### 6.3 Preview de efectos

**No en v0.2.** No se puede preescuchar un efecto sobre un source antes de componer. La complejidad de renderizar previews de efectos en tiempo real es demasiado alta. Se planea evaluacion para v0.3.

---

## 7. Timeline

### 7.1 Interaccion con eventos

El timeline en v0.2 es **solo visualizacion (read-only)**. No se pueden editar eventos directamente:

- **Click para seleccionar:** Si. El evento seleccionado se resalta con borde Amber (#FBAD17).
- **Doble click para info detallada:** Si. Abre un tooltip expandido o panel lateral con todos los datos del evento (source, duracion, amplitud, pan, efectos, distribucion usada, tecnica).
- **Arrastrar para mover:** No en v0.2.
- **Resize para cambiar duracion:** No en v0.2.
- **Delete para eliminar:** No en v0.2.

La edicion directa del timeline se evalua para v0.3. En v0.2, el flujo es: ajustar parametros -> Compose -> si no gusta, Re-roll o cambiar parametros.

### 7.2 Zoom y navegacion

- **Zoom horizontal (Ctrl+scroll):** Si. Permite ver mas o menos detalle temporal.
- **Zoom vertical:** No. El numero de tracks/layers es fijo en pantalla.
- **Scroll horizontal:** Si, con scroll normal o drag del eje temporal.
- **Minimap/overview:** No en v0.2. Se evalua para v0.3.

### 7.3 Informacion en hover

Al pasar el raton sobre un evento en el timeline, se muestra un tooltip con:

- **Nombre del source** (archivo de audio original)
- **Duracion** del evento (en segundos)
- **Amplitud** (valor normalizado 0-1)
- **Efectos aplicados** (lista de nombres)
- **Tecnica compositiva** usada para generar el evento

---

## 8. Render y exportacion

### 8.1 Render

- **Preescuchar antes de exportar (Play/Stop):** Si. Boton Play/Stop en la barra de transporte. Reproduce la composicion renderizada. Si no se ha renderizado aun, Render se ejecuta automaticamente al pulsar Play.
- **Duracion total y tamano estimado:** Si. Se muestra en la barra inferior: duracion total (mm:ss) y tamano estimado del archivo segun formato seleccionado.
- **Cancelar render en curso:** Si. Boton Cancel junto a la barra de progreso. Cancela el render y mantiene la composicion intacta.

### 8.2 Formatos de exportacion

> **v0.1:** WAV, MP3, FLAC

**v0.2:** Se mantienen los tres formatos de audio. No se anaden formatos de audio adicionales.

**Opciones de calidad:** Se mantienen las opciones existentes de v0.1 (bitrate para MP3, sample rate para WAV/FLAC). No se anaden opciones nuevas de calidad.

### 8.3 Exportacion de la composicion (no audio)

Se anaden dos nuevas opciones de exportacion no-audio:

- **Exportar composicion como JSON:** Guarda la composicion completa (todos los eventos con sus propiedades, timeline, metadata) como archivo `.json`. Permite recargar la composicion despues sin necesidad de recomponer. Formato: `composicion_[seed]_[timestamp].json`.
- **Exportar configuracion como JSON:** Guarda solo los parametros de configuracion (tecnica seleccionada, overrides, seed, sources con sus pesos) como archivo `.json`. Permite reproducir exactamente la misma pieza con las mismas sources. Formato: `config_[seed]_[timestamp].json`.

Ambas opciones estan disponibles en el menu Export junto a los formatos de audio.

---

## 9. Atajos de teclado

> **v0.1:** Ctrl+O (anadir audio), Ctrl+E (exportar), Ctrl+G (compose), Ctrl+R (re-roll), Ctrl+Q (salir)

Se mantienen todos los atajos de v0.1. Se anaden nuevos:

| Accion | Atajo v0.1 | Atajo v0.2 | Notas |
|--------|-----------|-----------|-------|
| Anadir audio | Ctrl+O | Ctrl+O | Sin cambios |
| Exportar | Ctrl+E | Ctrl+E | Sin cambios |
| Compose | Ctrl+G | Ctrl+G | Sin cambios |
| Re-roll | Ctrl+R | Ctrl+R | Sin cambios |
| Salir | Ctrl+Q | Ctrl+Q | Sin cambios |
| Render | (ninguno) | Ctrl+Shift+R | Nuevo |
| Play/Stop | (ninguno) | Space | Nuevo |
| Ciclar tecnica | (ninguno) | Ctrl+T | Nuevo — cicla entre las 12 tecnicas |
| Copiar seed | (ninguno) | Ctrl+Shift+C | Nuevo — copia seed al portapapeles |

---

## 10. Mensajes y feedback al usuario

### 10.1 Errores

> **v0.1:** QMessageBox para todo.

**v0.2:** Se mantiene **QMessageBox** para errores criticos y confirmaciones. No se implementan toast notifications en v0.2 — se planean para v0.3 como sistema de notificaciones no-bloqueantes para warnings y mensajes informativos.

### 10.2 Confirmaciones

Se pide confirmacion al usuario en los siguientes casos:

- **Al sobrescribir un archivo existente:** Si. Dialogo de confirmacion con nombre del archivo.
- **Al hacer Compose si ya hay una composicion sin exportar:** No. Compose sobreescribe la composicion anterior sin preguntar. El flujo iterativo (Compose -> ajustar -> Compose) debe ser fluido y sin fricciones. Si el usuario quiere guardar una composicion, debe exportarla antes.
- **Al cerrar la app con trabajo sin guardar:** Si. Dialogo de confirmacion si hay una composicion no exportada o una configuracion no guardada.

---

## 11. Funcionalidades nuevas en v0.2

### 11.1 Selector de tecnicas compositivas (tab Technique)

Tab dedicado con selector de 12 tecnicas compositivas (11 tecnicas + Custom/Blank). Al seleccionar una tecnica, se cargan defaults para strategy, structure, distribuciones, efectos y parametros especificos. Muestra en panel lateral los defaults que carga el preset y marca visualmente cuales han sido sobreescritos por el usuario (indicador Amber en parametros modificados).

### 11.2 Sistema de override de 6 capas

Pipeline jerarquico: TECHNIQUE -> STRATEGY -> STRUCTURE -> RNG -> EFFECTS, donde cada capa puede ser sobreescrita independientemente. Los parametros no sobreescritos mantienen los defaults de la tecnica. Permite al usuario empezar desde un preset razonable y refinar solo lo que necesita.

### 11.3 Exportacion JSON (composicion y configuracion)

Dos nuevas opciones de exportacion: composicion completa como JSON (para recargar) y configuracion como JSON (para reproducir). Detallado en seccion 8.3.

### 11.4 Curva de densidad custom (dibujable)

Sexta opcion de density curve que permite al usuario dibujar a mano libre. Detallado en seccion 4.3.

### 11.5 Theme: Design System v0.2

Tema oscuro mantenido pero con nuevo sistema de colores:
- **Amber (#FBAD17):** Acentos, seleccion, elementos interactivos activos, indicadores de override.
- **Slate (#303C42):** Fondos, paneles, elementos inactivos.
- **Teal (#005A65):** Secundario, headers, bordes de seccion, hover states.
- **Sand (#A69C95):** Texto secundario, labels, separadores.

Tipografia: **DM Serif Display** para titulos, **DM Mono** para valores numericos y seeds, **DM Sans** para texto general y labels.

---

## 12. Funcionalidades a eliminar

No se elimina ninguna funcionalidad de v0.1. Todo el comportamiento existente se mantiene. La tecnica "Custom/Blank" garantiza retrocompatibilidad total con el flujo original.

---

## 13. Organizacion de tabs

Referencia rapida de la distribucion de controles en los 3 tabs principales:

| Tab | Contenido |
|-----|-----------|
| **Composition** | Strategy selector, structure params, seed (campo + boton random), density curve selector + area custom |
| **Effects Palette** | 8 familias de efectos con toggle individual, slider de randomizacion por efecto, effects_probability global, max_effects_per_event |
| **Technique** | Selector de tecnica (12 opciones), panel de defaults del preset, indicadores de overrides activos, botones import/export de configuracion |
